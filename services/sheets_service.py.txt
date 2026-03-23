import requests
import logging
from config import config

logger = logging.getLogger(__name__)

class SheetsService:
    def __init__(self):
        self.url = config.GOOGLE_SCRIPT_URL
    
    def _call(self, action, data=None):
        try:
            payload = {"action": action}
            if data:
                payload.update(data)
            
            response = requests.post(
                self.url,
                json=payload,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Sheets Error: {e}")
            return {"success": False, "error": str(e)}
    
    def get_productos(self, categoria=None, solo_stock=True):
        data = {"solo_stock": solo_stock}
        if categoria:
            data["categoria"] = categoria
        result = self._call("get_productos", data)
        return result.get('productos', [])
    
    def get_producto(self, sku):
        result = self._call("get_producto", {"sku": sku})
        return result.get('producto') if result.get('success') else None
    
    def check_stock(self, sku, cantidad):
        return self._call("check_stock", {"sku": sku, "cantidad": cantidad})

sheets = SheetsService()
