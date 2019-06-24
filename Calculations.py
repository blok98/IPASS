def convertHeightToCM(height_in_feet_and_inches):
    if str(height_in_feet_and_inches)=="nan":
        return 0.00
    height=str(height_in_feet_and_inches).split("'")
    height_in_cm=int(height[0])*30.48+int(height[1])*2.54
    return round(height_in_cm,2)

def convertWeightToKG(weight_in_lbs):
    if str(weight_in_lbs)=="nan":
        return 0.00
    weight=str(weight_in_lbs).split("l")
    weight_in_kg=int(weight[0])*0.45359237
    return round(weight_in_kg,2)