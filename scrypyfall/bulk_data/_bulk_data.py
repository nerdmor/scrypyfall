import os
from time import sleep
from typing import Any
from typing import NewType

import requests

from scrypyfall.foundation import ScrypyfallFoundation
from scrypyfall.foundation import ScrypyfallIterableFoundation
from scrypyfall.settings import settings

CHUNK_SIZE = 8192


Bulk_data = NewType('Bulk_data', ScrypyfallIterableFoundation)
BulkDataItem = NewType('BulkDataItem', ScrypyfallFoundation)


class Bulk_data(ScrypyfallIterableFoundation):
    def __init__(self) -> None:
        super().__init__('bulk-data')
        self.bulk_data_item = BulkDataItem()

        # TODO: pull the kinds and IDs currently available to make them into anonymnour functions
    
    def __call__(self, id:str = None, type_:str = None, **kwargs:Any) -> Bulk_data:      
        if id:
            return self.id(id, **kwargs)
        if type_:
            return self.type(type_, **kwargs)

        return self.make_request(headers=kwargs.get('headers'))
    
    def id(self, id:str, format:str = 'json',  file_dir:str = None, **kwargs: Any) -> BulkDataItem:
        return self.bulk_data_item.get(identifier_type='id',
                                       identifier=id,
                                       format=format,
                                       file_dir=file_dir)

    def type(self, type_:str, format:str = 'json',  file_dir:str = None, **kwargs: Any) -> BulkDataItem:
        return self.bulk_data_item.get(identifier_type='type',
                                       identifier=type_,
                                       format=format,
                                       file_dir=file_dir)
    

class BulkDataItem(ScrypyfallFoundation):
    def __init__(self) -> None:
        super().__init__('bulk-data')
    
    def get(self, identifier_type:str, identifier:str, format:str = 'json', file_dir:str = None, **kwargs: Any) -> dict:
        if identifier_type not in ['id', 'type']:
            raise ValueError('Invalid identifier type')

        self.accepted_params = {
            'format': {'type': str, 'options': ['json', 'file']}
        }

        self.data = self.make_request(identifier, headers=kwargs.get('headers'))

        if format == 'json':
            return self.data
        
        # downloading the file
        save_path = os.getcwd()
        file_name = self.data['download_uri'].split('/')[-1]
        if file_dir:
            if os.path.isabs(file_dir):
                save_path = file_dir
            elif os.path.isdir(os.path.join(os.getcwd(), file_dir)):
                save_path = os.path.join(os.getcwd(), file_dir)
        
        save_path = os.path.join(save_path, file_name)
        self.data['file_path'] = save_path

        sleep(settings.sleep_time)
        with requests.get(self.data['download_uri'], stream=True) as r:
            r.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=settings.chunk_size):
                    f.write(chunk)

        return self.data

        
