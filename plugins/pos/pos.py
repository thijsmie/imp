import pluginbase
pluginsource = pluginbase.find_plugin_source()

if (pluginsource == None):
    print("This plugin cannot be executed directly")
    import sys
    sys.exit()

app = pluginsource.appdata['app']
security = pluginsource.appdata['security']
protected = security.protected

@app.route('/pos/{id}/add', methods=["POST"])
def pos_add_stock(id):
    pass
    
@app.route('/pos/{id}/sell', methods=["POST"])
def pos_sell_stock(id):
    pass
    
@app.route('/pos/{id}/skim', methods=["POST"])
def pos_skim_income(id):
    pass
    
@app.route('/pos/{id}/spoil', methods=["POST"])
def pos_spoil_stock(id):
    pass
    
@app.route('/pos/{id}/diff', methods=["POST"])
def pos_lost_money(id):
    pass
    
@app.route('/pos/{id}/auth', methods=["POST"])
def pos_authorize(id):
    pass
    
@app.route('/pos/{id}', methods=["GET"])
def pos_info(id):
    pass
    
@app.route('/pos', methods=["POST"])
def pos_create():
    pass
