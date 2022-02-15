class College:

    def __init__(self, name=""):
        self.name = name
        self.data = {"name": self.name}

    @staticmethod
    def clean(data):
        if data == 'No data available \xa0':
            return None
        elif isinstance(data, str):
            processed = data.translate({ord(c): None for c in "$%,"})
            if processed.isdigit():
                return int(processed)
            return data

    def add_score(self, score_type, score):
        score_range = score.split("-")
        try:
            self.data[score_type + "_low"] = int(score_range[0])
            self.data[score_type + "_high"] = int(score_range[1])
        except (KeyError, IndexError):
            self.data[score_type + "_low"] = None
            self.data[score_type + "_high"] = None

    def add_data(self, action, data):
        try:
            self.data[action] = self.clean(data)
        except (KeyError, IndexError):
            self.data[action] = None

    def add_location(self, data):
        try:
            self.data["area"] = data[:-4].title()
            self.data["state"] = data[-2:]
        except (KeyError, IndexError):
            self.data["area"] = None
            self.data["state"] = None

    def add_major(self, data):
        for i in range(len(data)):
            try:
                self.data[f"major_{i+1}"] = data[i][0]
            except (KeyError, IndexError):
                self.data[f"major_{i + 1}"] = None

            try:
                self.data[f"major_{i+1}_graduates"] = self.clean(data[i][1][:-10])
            except (KeyError, IndexError):
                self.data[f"major_{i + 1}_graduates"] = None
