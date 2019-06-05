
class EvaluationTable:
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame
        self.stats = statEval(dataFrame)


def statEval(dataFrame):
        # statistical evaluation of dataframe
        desc = dataFrame.describe()
        filt_desc = desc.loc[['mean', 'std', 'min', 'max'], :]
        return filt_desc
