# -*- coding: utf-8 -*-

import cPickle
import logging

from ...shared.model_names import SYNC_DATA_FIELD
from ...models_access import OdooProductAccess

_logger = logging.getLogger(__name__)


class UpdateTransformer(object):
    """
    This class transform update values to update message fields
    """
    def __init__(self, env):
        self._odoo_product = OdooProductAccess(env)

    def _convert_update(self, sync_update):
        sync_value = {}
        sync_data = cPickle.loads(sync_update[SYNC_DATA_FIELD])
        sync_value['ID'] = sync_update.id
        # SKU can not be changed after creation
        sync_value['SKU'] = self._odoo_product.get_sku(sync_update)
        sync_value['Title'] = sync_data['name']

        return sync_value

    def transform(self, sync_updates):
        sync_values = []
        for sync_update in sync_updates:
            sync_value = self._convert_update(sync_update)
            if sync_value:
                sync_values.append(sync_value)
        return sync_values