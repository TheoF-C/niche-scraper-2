class College:

    def __init__(self, name=""):
        self.name = name
        self.data = {"name": self.name}

    @staticmethod
    def clean(data):
        if data == 'No self.data available \xa0':
            print(data)
            return None
        elif isinstance(data, str):
            processed = data.translate({ord(c): None for c in "$%,"})
            if processed.isdigit():
                return int(processed)
            return data

    def add_score(self, score_type, score):
        score_range = score.split("-")
        self.data[score_type + "_low"] = int(score_range[0])
        self.data[score_type + "_high"] = int(score_range[1])

    def add_data(self, action, data):
        if action in ["sat", "act"]:
            self.add_score(action, data)
            return
        self.data[action] = self.clean(data)

    def add_location(self, data):
        self.data["area"] = data[:-4].title()
        self.data["state"] = data[-2:]

    def add_major(self, data):
        for i in range(len(data)):
            self.data[f"major_{i+1}"] = data[i][0]
            self.data[f"major_{i+1}_graduates"] = self.clean(data[i][1][:-10])

