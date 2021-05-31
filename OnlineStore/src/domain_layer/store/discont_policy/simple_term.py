from OnlineStore.src.domain_layer.store.discont_policy.term import Term


class SimpleTerm(Term):

    def __init__(self):
        self.stam = 3

    def calc_term(self, basketDTO):
        return True





