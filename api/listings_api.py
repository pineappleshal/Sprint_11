class ListingsApi:
    def __init__(self, client, token):
        self.client = client
        self.token = token

    def create(self, data):
        return self.client.request('POST', '/create-listing', token=self.token, form=data)

    def update(self, listing_id, data):
        form = {**data, 'img1': 'null', 'img2': 'null', 'img3': 'null'}
        return self.client.request('PATCH', f'/update-offer/{listing_id}', token=self.token, form=form)

    def get_own(self):
        return self.client.request('GET', '/profile/listings/1', token=self.token)

    def delete(self, listing_id):
        return self.client.request('DELETE', f'/listings/{listing_id}', token=self.token)
