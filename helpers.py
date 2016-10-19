from .application import db

def calculate_transaction_totals(self, transaction):
    producttotals = {}
    _modtotals = {}
    total = 0.
    
    for row in transaction.rows:
        if row.product.group in producttotals:
            producttotals[row.product.group] += row.value
        else
            producttotals[row.product.group] = row.value
        
        total += row.value
        
        if row.value < 0:
            mods = row.product.losemods
        elif row.value > 0:
            mods = row.product.gainmods
            
        for mod in mods:
            if not mod in row.exclude_mods:
                modvalue = mod.apply(row.amount, row.value)
                if mod.name in modtotals:
                    _modtotals[mod] += modvalue
                else:
                    _modtotals[mod] = modvalue
    
    modtotals = {}
    for k, v in _modtotals.iteritems():
        modtotals[k.name] = round(v)
        if not k.included:
            total += round(v)
            
    return {'total': total, 'producttotals': producttotals, 'modtotals': modtotals}

    
        
        
        
