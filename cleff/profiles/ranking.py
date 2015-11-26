"""
    This is a file for all ranking functions for the cleffapp profiles app
"""


def update_instrument_rank(instrument_obj):
    instrument = instrument_obj
    num = instrument.numerator
    den = instrument.denominator
    r = num/den
    instrument.rank = r
    instrument.save()
