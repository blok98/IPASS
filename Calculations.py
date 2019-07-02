from random import sample

class Calculations:

    def __init__(self):
        pass

    def convertHeightToCM(self,height_in_feet_and_inches):
        if str(height_in_feet_and_inches) == "nan":
            return 0.00
        height = str(height_in_feet_and_inches).split("'")
        height_in_cm = int(height[0]) * 30.48 + int(height[1]) * 2.54
        return round(height_in_cm, 2)

    def convertWeightToKG(self,weight_in_lbs):
        if str(weight_in_lbs) == "nan":
            return 0.00
        weight = str(weight_in_lbs).split("l")
        weight_in_kg = int(weight[0]) * 0.45359237
        return round(weight_in_kg, 2)

    def seperateData(self,match_coll, train=0.7, test=0.3):
        match_train = sample(match_coll, int(0.7 * len(match_coll)))
        match_test = [match for match in match_coll if match not in match_train]
        return match_train, match_test
