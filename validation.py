from jsonschema import validate

NewTransactionRowSchema = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "enum": ["gain", "lose"]},
        "product": {"type": "integer"},
        "amount":  {"type": "integer"},
        "value":   {"type": "integer"},
        "exclude_mods":    {
            "type": "array", 
            "items": {"type": "integer"}
            }
    },
    "required": ["product", "amount", "type"]
}

def NewTransactionRowValidator(data):
    return validate(data, NewTransactionRowSchema)

EditTransactionRowSchema = {
    "type": "object",
    "properties": {
        "index": {"type": "integer"},
        "product": {"type": "integer"},
        "amount":  {"type": "integer"},
        "value":   {"type": "integer"},
        "exclude_mods":    {
            "type": "array", 
            "items": {"type": "integer"}
            }
    },
    "required": ["index"]
}

def EditTransactionRowValidator(data):
    return validate(data, EditTransactionRowSchema)

NewTransactionSchema = {
    "type": "object",
    "properties": {
        "eventname": {"type": "string"},
        "eventdate": {"type": "string"},
        "eventcontact": {"type": "string"},
        "eventnotes": {"type": "string"},
        "rows": {
            "type": "array",
            "minItems": 1,
            "items": NewTransactionRowSchema
        }
    },
    "required": ["eventname", "eventdate", "eventcontact", "rows"]
}

def NewTransactionValidator(data):
    return validate(data, NewTransactionSchema)

EditTransactionSchema = {
    "type": "object",
    "properties": {
        "index": {"type": "integer"},
        "eventname": {"type": "string"},
        "eventdate": {"type": "string"},
        "eventcontact": {"type": "string"},
        "eventnotes": {"type": "string"},
        "rows": {
            "type": "array",
            "minItems": 1,
            "items": NewTransactionRowSchema
        }
    },
    "required": ["index"]
}

def EditTransactionValidator(data):
    return validate(data, EditTransactionSchema)

NewModSchema = {
    "type": "object",
    "properties": {
        "name":       {"type": "string"},
        "pre_add":    {"type": "integer"},
        "multiplier": {"type": "number"},
        "post_add":   {"type": "integer"},
        "included":   {"type": "boolean"}
    },
    "required": ["name", "included"]
}

EditModSchema = {
    "type": "object",
    "properties": {
        "index":      {"type": "integer"},
        "name":       {"type": "string"},
        "pre_add":    {"type": "integer"},
        "multiplier": {"type": "number"},
        "post_add":   {"type": "integer"},
        "included":   {"type": "boolean"}
    },
    "required": ["index"]
}

NewRelationSchema = {
    "type": "object",
    "properties": {
        "name":     {"type": "string"},
        "email":    {"type": "string"},
        "budget":   {"type": "integer"},
        "send_transaction":         {"type": "boolean"},
        "send_transaction_updates": {"type": "boolean"},
        "send_budget_warnings":     {"type": "boolean"}
    },
    "required": ["name", "email"]
}

EditRelationSchema = {
    "type": "object",
    "properties": {
        "index":    {"type": "integer"},
        "name":     {"type": "string"},
        "email":    {"type": "string"},
        "budget":   {"type": "integer"},
        "send_transaction":         {"type": "boolean"},
        "send_transaction_updates": {"type": "boolean"},
        "send_budget_warnings":     {"type": "boolean"}
    },
    "required": ["index"]
}
