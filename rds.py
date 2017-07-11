

class RdsDbInstance:
    
    def __init__(self, session):
        self.rds_client = session.client("rds")

    def get_rds_instances(self):

        rds_instance_list = []

        rds_instances = self.rds_client.describe_db_instances()

        for instance in rds_instances["DBInstances"]:
            rds_instance_list.append("{}".format(instance["DBInstanceIdentifier"]))

        return rds_instance_list

    def stop_rds_instance(self, rds_instance):

        state = self.get_rds_instance_state(rds_instance)

        if state == "available":
            result = "-- Stopping DB Instance \"{}\"".format(rds_instance)
            self.rds_client.stop_db_instance(
                DBInstanceIdentifier=rds_instance,
            )

        elif state == "stopped":
            result = "-- DB instance \"{}\" is already stopped.".format(rds_instance)

        else:
            result = "-- Unable to stop DB instance \"{}\" in state {}".format(rds_instance, state)

        return result

    def start_rds_instance(self, rds_instance):

        state = self.get_rds_instance_state(rds_instance)

        if state == "stopped":
            result = "-- Starting DB instance \"{}\"".format(rds_instance)
            self.rds_client.start_db_instance(
                DBInstanceIdentifier=rds_instance,
            )

        elif state == "available":
            result = "-- DB instance \"{}\" is already running.".format(rds_instance)

        else:
            result = "-- Unable to start DB instance \"{}\" in state {}".format(rds_instance, state)

        return result

    def get_rds_instance_state(self, rds_instance):

        state = self.rds_client.describe_db_instances(
            DBInstanceIdentifier=rds_instance,
        )["DBInstances"][0]["DBInstanceStatus"]

        return state
