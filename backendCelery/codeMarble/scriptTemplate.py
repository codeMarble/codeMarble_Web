from placementRule import PlacementRule
from actionRule import ActionRule
from endingRule import EndingRule

class UserRule(PlacementRule, ActionRule, EndingRule):
    def __init__(self):
        PlacementRule.__init__(self)
        ActionRule.__init__(self)
        EndingRule.__init__(self)