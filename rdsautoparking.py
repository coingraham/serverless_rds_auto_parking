import boto3
import datetime
from rds import RdsDbInstance
from ddb import DdbInstance


class RdsAutoParking:
    
    def __init__(self, _table, _region):
        print "** Starting RDS Auto Parking Utility. **\n"
        self.result = ""
        self.table = _table
        self.session = boto3.session.Session(region_name=_region)
        # self.session = boto3.session.Session(region_name=_region, profile_name="myprofile") # for local testing
        self.rds_instance_list = []
        self.ddb = None
        self.rds = None

    def check_configuration(self):
        print "** Checking RDS configurations. **\n"

        missing_rds_config_list = []

        self.ddb = DdbInstance(self.session, self.table)

        rds_in_config_list = self.ddb.get_rds_instances_in_ddb()

        self.rds = RdsDbInstance(self.session)

        self.rds_instance_list = self.rds.get_rds_instances()

        for rds_instance in self.rds_instance_list:
            if rds_instance not in rds_in_config_list:
                missing_rds_config_list.append(rds_instance)

        if len(missing_rds_config_list) > 0:
            print "** Adding missing RDS instances into DynamoDB configuration. **"
            self.ddb.build_config(missing_rds_config_list)

        print "** All RDS instances configured in DynamoDB table. **\n"

    def auto_park_rds(self):
        print "** Starting RDS Auto Parking Job. **"
        today = datetime.date.today().strftime("%A")

        for rds_instance in self.rds_instance_list:
            print "\n-- Evaluating DB instance \"{}\" for auto parking.".format(rds_instance)
            config = self.ddb.get_rds_instance_config_for_day(rds_instance, today)

            if config["exclude"]["S"] == "True":
                print "-- DB instance \"{}\" excluded from auto parking.".format(rds_instance)
                continue

            print self.assess_config_and_act(rds_instance, config)

        print "\n** RDS Auto Parking Utility Complete. **\n"

    def assess_config_and_act(self, rds_instance, config):

        if config["all_day"]["S"] == "On":
            print "-- DB Instance \"{}\" marked for \"On\" all day.  Starting.".format(rds_instance)
            return self.rds.start_rds_instance(rds_instance)

        elif config["all_day"]["S"] == "Off":
            print "-- DB Instance \"{}\" marked for \"Off\" all day.  Stopping.".format(rds_instance)
            return self.rds.stop_rds_instance(rds_instance)

        now = datetime.datetime.now()
        start_time = now.replace(hour=int(config["start_hour"]["N"]), minute=0, second=0, microsecond=0)
        stop_time = now.replace(hour=int(config["stop_hour"]["N"]), minute=0, second=0, microsecond=0)

        if start_time <= now <= stop_time:
            print "-- Current time is in between start/stop times. Starting DB instance \"{}\".".format(rds_instance)
            return self.rds.start_rds_instance(rds_instance)
        else:
            print "-- Current time is outside of start/stop times.  Stopping DB instance \"{}\".".format(rds_instance)
            return self.rds.stop_rds_instance(rds_instance)

    def main(self):

        self.check_configuration()

        self.auto_park_rds()
