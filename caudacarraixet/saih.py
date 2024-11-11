import requests




class SAIHClient:

    def __init__(self):
        self.url = "https://saih.chj.es/chj/saih/stats/datosGrafico?v=0O01DQG2MVVR&t=ultimos5minutales"
        self.max_carraixet_flow = 1_250  # m3/s

    def get_carraixet_flow(self):

        response = requests.request("GET", self.url)

        if not response.ok:
            print(f"Error {response.status_code}")
            print(f"Error {response.text}")
            return None

        data = response.json()

        flow_trend = self._calculate_trend(data)
        current_flow_value = data[1][0][1]
        current_flow_time = data[1][0][0]

        dimension = data[0]['dimension']

        description = data[0]['descripcion']

        saih_response = {
            "description": description,
            "dimension": dimension,
            "current_flow_value": current_flow_value,
            "current_flow_time": current_flow_time,
            "flow_trend": flow_trend,
            "max_carraixet_flow": self.max_carraixet_flow
        }

        return saih_response

    def _calculate_trend(self, data):
        values = data[1]

        most_recent_value = values[0][1]
        least_recent_value = values[-1][1]

        trend = most_recent_value - least_recent_value

        if trend > 0:
            return "Creciendo"
        elif trend < 0:
            return "Decreciendo"

        # TODO Añadir cálculo de la velocidad de crecimiento
        return trend


if __name__ == '__main__':
    response = SAIHClient().get_carraixet_flow()

    print(response)
