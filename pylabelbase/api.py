import requests
import json


class LabelbaseAPI:
    """
    base_url =
        Cloud-hostet: https://labelbase.space/api/v0
        Localhost: http://127.0.0.1:8080/api/v0
    """
    def __init__(self, api_key, base_url="https://labelbase.space/api/v0"):
        self.base_url = base_url
        self.session = requests.Session()
        self.current_labelbase_id = None
        self.headers = {
            'Authorization': f'Token {api_key}'
        }

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}/"
        try:
            response = self.session.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            if response.text:
                return response.json()
            return None
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None
        except ValueError:
            print("Failed to decode JSON")
            return None

    def _get_labelbase_id(self, labelbase_id=None):
        """ Helper to determine the correct labelbase ID to use. """
        if labelbase_id:
            return labelbase_id
        elif self.current_labelbase_id:
            return self.current_labelbase_id
        else:
            raise ValueError("No labelbase ID provided and no current labelbase selected.")

    def use_labelbase(self, labelbase_id):
        """ Change current active labelbase. """
        self.current_labelbase_id = labelbase_id
        print(f"Labelbase changed, current ID is {self.current_labelbase_id}.")

    def list_labelbases(self):
        """ List labelbases """
        resp = self._request("GET", "labelbase")
        return resp

    def get_labelbase(self, labelbase_id):
        """ Retrieve labelbase with the given id. """
        resp = self._request("GET", f"labelbase/{labelbase_id}")
        return resp

    def create_labelbase(self, name="", fingerprint="", about="", use_created=True):
        """ Create a new labelbase. """
        data = {
            'name': name,
            'fingerprint': fingerprint,
            'about': about
        }
        resp = self._request("POST", "labelbase", data=data)
        new_labelbase_id = resp.get('id')
        print(f"Labelbase created, created ID is {new_labelbase_id}.")
        if use_created:
            self.use_labelbase(new_labelbase_id)
        return resp

    def update_labelbase(self, labelbase_id=None, name="", fingerprint="", about="", use_updated=True):
        """ Update an existing labelbase. """
        lb_id = self._get_labelbase_id(labelbase_id)
        data = {
            'name': name,
            'fingerprint': fingerprint,
            'about': about
        }
        resp = self._request("PUT", f"labelbase/{lb_id}", data=data)
        new_labelbase_id = resp.get('id')
        if use_updated:
            self.use_labelbase(new_labelbase_id)
        return resp

    def delete_labelbase(self, labelbase_id=None):
        """ Delete the specified labelbase or current labelbase. """
        lb_id = self._get_labelbase_id(labelbase_id)
        resp = self._request("DELETE", f"labelbase/{lb_id}")
        return resp

    def list_labels(self, labelbase_id=None):
        """ List labels of the specified labelbase or current labelbase. """
        lb_id = self._get_labelbase_id(labelbase_id)
        endpoint = f"labelbase/{lb_id}/label"
        return self._request("GET", endpoint)

    def create_label(self, *args, labelbase_id=None, **kwargs):
        """
        Create a new label within the specified labelbase or current labelbase.
        Can be called with a data dictionary or with individual arguments.

        The origin parameter is allowed only when type is 'tx'.
        The spendable parameter is allowed only when type is 'output'.

        With a dictionary:

                create_label(label_id, data, labelbase_id=...)

        With individual keyword arguments:

                create_label(label_id, label_type='type',
                             ref='ref', label='label', labelbase_id=...)

        """
        lb_id = self._get_labelbase_id(labelbase_id)
        if args and isinstance(args[0], dict):
            data = args[0]
        elif kwargs:
            data = kwargs
        else:
            raise ValueError("No data provided for label creation.")
        if 'type' in data:
            if data['type'] != 'tx' and 'origin' in data:
                raise ValueError("'origin' is only valid when 'type' is 'tx'")
            if data['type'] != 'output' and 'spendable' in data:
                raise ValueError("'spendable' is only valid when 'type' is 'output'")
        endpoint = f"labelbase/{lb_id}/label"
        return self._request("POST", endpoint, data=data)

    def update_label(self, label_id, labelbase_id=None, **kwargs):
        """
        Update a specific label within the specified labelbase or current labelbase.
        """
        lb_id = self._get_labelbase_id(labelbase_id)
        existing_label_data = self.get_label(label_id, lb_id)
        if not existing_label_data:
            print("Error: Label data could not be retrieved.")
            return None
        updated_data = {**existing_label_data, **kwargs}
        label_type = updated_data.get('type')
        if label_type != 'output' and 'spendable' in updated_data:
            del updated_data['spendable']
        endpoint = f"labelbase/{lb_id}/label/{label_id}"
        return self._request("PUT", endpoint, data=updated_data)

    def get_label(self, label_id, labelbase_id=None):
        """ Read a specific label from the specified labelbase or current labelbase. """
        lb_id = self._get_labelbase_id(labelbase_id)
        endpoint = f"labelbase/{lb_id}/label/{label_id}"
        return self._request("GET", endpoint)

    def delete_label(self, label_id, labelbase_id=None):
        """ Delete a specific label from the specified labelbase or current labelbase. """
        lb_id = self._get_labelbase_id(labelbase_id)
        endpoint = f"labelbase/{lb_id}/label/{label_id}"
        return self._request("DELETE", endpoint)

    def find_label_by_ref_and_type(self, ref, type, labelbase_id=None):
        """
        Find the first label by its reference and type.

        NOTE: A labelbase may have multiple labels with the same reference and type combination.
        """
        lb_id = self._get_labelbase_id(labelbase_id)
        labels = self.list_labels(lb_id)
        for label in labels:
            if label.get('ref') == ref and label.get('type') == type:
                return label
        return None

    def get_or_create_label_by_ref_and_type(self, ref, type, labelbase_id=None, **kwargs):
        """
        Get the first label by ref and type, or create it if it doesn't exist.

        NOTE: A labelbase may have multiple labels with the same reference and type combination.
        """
        label = self.find_label_by_ref_and_type(ref, type, labelbase_id)
        if label:
            return label
        else:
            data = {'ref': ref, 'type': type}
            data.update(kwargs)
            return self.create_label(labelbase_id=labelbase_id, **data)

    def update_or_create_label_by_ref_and_type(self, ref, type, labelbase_id=None, **kwargs):
        """
        Update the first label by ref and type, or create it if it doesn't exist.

        NOTE: A labelbase may have multiple labels with the same reference and type combination.
        """
        label = self.find_label_by_ref_and_type(ref, type, labelbase_id)
        if label:
            label_id = label.get('id')
            existing_data = self.get_label(label_id, labelbase_id)
            if existing_data:
                # Update only provided fields, preserve existing ones
                updated_data = {**existing_data, **kwargs}
                # Remove invalid fields based on the label type
                if type != 'output' and 'spendable' in updated_data:
                    del updated_data['spendable']
                if type != 'tx' and 'origin' in updated_data:
                    del updated_data['origin']
                return self.update_label(label_id, labelbase_id=labelbase_id, **updated_data)
            else:
                print("Error: Existing label data could not be retrieved.")
                return None
        else:
            data = {'ref': ref, 'type': type}
            data.update(kwargs)
            return self.create_label(labelbase_id=labelbase_id, **data)
