

class DdbInstance:
    
    def __init__(self, session, _table):
        self.ddb_client = session.client("dynamodb")
        self.days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.table = _table

    def get_rds_instances_in_ddb(self):

        rds_instance_set = set()

        ddb_records = self.ddb_client.scan(TableName=self.table)["Items"]

        for ddb_record in ddb_records:
            rds_instance_set.add(ddb_record["rds_instance"]["S"])

        return rds_instance_set

    def get_rds_instance_config_for_day(self, _rds_instance, _day):

        ddb_record = self.ddb_client.get_item(
            TableName=self.table,
            Key={
                'rds_instance': {'S': str(_rds_instance)},
                'day_of_week': {'S': str(_day)}
            }
        )["Item"]

        return ddb_record

    def build_config(self, rds_missing_config_list):

        for rds_missing_config in rds_missing_config_list:
            for day in self.days:
                self.ddb_client.put_item(
                    TableName=self.table,
                    Item={
                        u"all_day": {u"S": u"On"},
                        u"exclude": {u"S": u"True"},
                        u"day_of_week": {u"S": day},
                        u"rds_instance": {u"S": rds_missing_config},
                        u"start_hour": {u"N": u"9"},
                        u"stop_hour": {u"N": u"21"}
                    }
                )

            print "-- Config updated for {}".format(rds_missing_config)
