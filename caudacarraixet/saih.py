import requests
import logging



class SAIHClient:

    def __init__(self):
        self.url = "https://saih.chj.es/chj/saih/stats/datosGrafico?v=0O01DQG2MVVR&t=ultimos5minutales"
        self.max_carraixet_flow = 1_250  # m3/s
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("SAIH Client initialized")

    def get_carraixet_flow(self):

        response = requests.request("GET", self.url)

        if not response.ok:
            self.logger.error(f"Error {response.status_code}")
            self.logger.error(f"Error {response.text}")
            return None

        data = response.json()

        values = data[1]

        sanitized_values = [ (x[0], x[1]) for x in values if x[1] is not None]

        flow_trend = self._calculate_trend(sanitized_values)
        current_flow_value = sanitized_values[0][1]
        current_flow_time = sanitized_values[0][0]
        dimension = data[0]['dimension']
        description = data[0]['descripcion']
        warning = self._warning_message(current_flow_value)

        saih_response = {
            "description": description,
            "dimension": dimension,
            "current_flow_value": current_flow_value,
            "current_flow_time": current_flow_time,
            "flow_trend": flow_trend,
            "max_carraixet_flow": self.max_carraixet_flow,
            "warning": warning
        }

        self.logger.info(f"SAIH Response: {saih_response}")

        return saih_response

    def _warning_message(self, current_flow_value):

        if current_flow_value > self.max_carraixet_flow:
            return "El caudal actual supera el límite máximo".upper()
        elif current_flow_value > self.max_carraixet_flow * 0.8:
            return "El caudal actual está por encima del 80%".upper()
        else:
            return None

    def _calculate_trend(self, values):

        most_recent_value = values[0][1]
        least_recent_value = values[-1][1]

        trend = most_recent_value - least_recent_value

        if trend > 0:
            return "Creciendo"
        elif trend < 0:
            return "Decreciendo"
        else:
            return "Estable"

        # TODO Añadir cálculo de la velocidad de crecimiento
        return trend


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    response = SAIHClient().get_carraixet_flow()

    print(response)
