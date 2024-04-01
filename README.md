# pylabelbase
[pylabelbase](https://github.com/Labelbase/pylabelbase) is the official API wrapper for [labelbase.space](https://labelbase.space), the open-source Bitcoin BIP-329 label management platform.

## Installation
```
~pip install pylabelbase~ soon
```


## Usage

First, import pylabelbase and initialize with your API key:

```
from pylabelbase import LabelbaseAPI

api_key = "your_api_key" # https://labelbase.space/account/apikey/ 
api = LabelbaseAPI(api_key) # cloud-hosted Labelbase
api = LabelbaseAPI(api_key, base_url="http://127.0.0.1:8080/api/v0") # your locally hosted Labelbase

```

## Working with Labelbases 

```
# List all labelbases
labelbases = api.list_labelbases()

# Create a new labelbase
new_labelbase = api.create_labelbase(name="New Labelbase")

# Update a labelbase
api.update_labelbase(labelbase_id=1, name="Updated Name")

# Change current active labelbase
api.use_labelbase(labelbase_id=2)

# Delete a labelbase
api.delete_labelbase(labelbase_id=1)

```

## Managing Labels (CRUD)
```
# Create a new label
label = api.create_label(label_type="tx", ref="transaction_ref", label="Transaction Label")

# Get (read) a label
retrieved_label = api.get_label(label_id=label['id'])

# Update a label
api.update_label(label_id=label['id'], label="Updated Label")

# Delete a label
api.delete_label(label_id=label['id'])

```

## Additional Features

### Find Label by Reference and Type
The `find_label_by_ref_and_type` method allows you to find the first label that matches a given reference and type within a labelbase. This is particularly useful in scenarios where a labelbase might have multiple labels with the same reference and type combination.

```
label = api.find_label_by_ref_and_type(ref="reference_here", type="type_here")
``` 

### Get or Create Label by Reference and Type

The `get_or_create_label_by_ref_and_type` method retrieves the first label that matches the provided reference and type. If no such label exists, it creates a new label with the specified parameters.

```
label = api.get_or_create_label_by_ref_and_type(ref="reference_here", type="type_here", additional_param1="value1")

```

### Update or Create Label by Reference and Type
The `update_or_create_label_by_ref_and_type` method updates the first label matching the specified reference and type. If no label is found, it creates a new label. This method ensures that only the intended fields are updated, while others remain unchanged.


```
label = api.update_or_create_label_by_ref_and_type(ref="reference_here", type="type_here", additional_param1="value1")
```


# License
[pylabelbase](https://github.com/Labelbase/pylabelbase) is released under the MIT License.

# Support the Project
If you find labelbase.space or [pylabelbase](https://github.com/Labelbase/pylabelbase) useful and would like to support its ongoing development, consider making a donation.

👉 [geyser.fund/project/labelbase](https://geyser.fund/project/labelbase)

