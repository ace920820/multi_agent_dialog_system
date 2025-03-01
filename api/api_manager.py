"""
API管理器模块 - 负责管理和调用外部API服务
"""
import logging
import json
import os
import requests
from typing import Dict, List, Any, Optional, Union, Callable
from requests.exceptions import RequestException
import time
import traceback

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ApiManager:
    """
    API管理器
    
    负责管理和调用外部API服务，包括错误处理、重试机制和缓存管理
    """
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        初始化API管理器
        
        Args:
            base_url: API服务的基础URL，如果为None则从环境变量获取
            api_key: API密钥，如果为None则从环境变量获取
        """
        # 从环境变量或参数获取配置
        self.base_url = base_url or os.getenv('API_BASE_URL', '')
        self.api_key = api_key or os.getenv('API_KEY', '')
        
        # 重试配置
        self.max_retries = 3
        self.retry_delay = 1.0  # 秒
        
        # 缓存配置
        self.use_cache = True
        self.cache_dir = '.api_cache'
        self.cache_expiration = 3600  # 1小时
        
        # 请求头
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}' if self.api_key else ''
        }
        
        # 初始化缓存目录
        if self.use_cache and not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)
            
        logger.info(f"API管理器初始化完成，基础URL: {self.base_url[:30]}{'...' if len(self.base_url) > 30 else ''}")
        
    def call_api(self, endpoint: str, method: str = 'GET', 
                params: Optional[Dict[str, Any]] = None, 
                data: Optional[Dict[str, Any]] = None,
                headers: Optional[Dict[str, str]] = None,
                retry: bool = True,
                use_cache: Optional[bool] = None) -> Dict[str, Any]:
        """
        调用API接口
        
        Args:
            endpoint: API接口路径
            method: 请求方法
            params: URL参数
            data: 请求数据
            headers: 自定义请求头
            retry: 是否在出错时重试
            use_cache: 是否使用缓存，如果为None则使用全局设置
            
        Returns:
            API响应数据，出错时返回包含错误信息的字典
        """
        # 合并请求头
        merged_headers = self.headers.copy()
        if headers:
            merged_headers.update(headers)
            
        # 确定是否使用缓存
        use_cache = self.use_cache if use_cache is None else use_cache
        
        # 对于GET请求，尝试从缓存获取
        if use_cache and method.upper() == 'GET':
            cache_result = self._get_from_cache(endpoint, params)
            if cache_result:
                logger.info(f"从缓存获取到结果: {endpoint}")
                return cache_result
                
        # 构建完整URL
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        # 执行请求，支持重试
        retries = self.max_retries if retry else 1
        last_error = None
        
        for attempt in range(retries):
            try:
                logger.info(f"调用API: {method} {endpoint}")
                logger.debug(f"参数: {params}, 数据: {data}")
                
                response = requests.request(
                    method=method.upper(),
                    url=url,
                    params=params,
                    json=data,
                    headers=merged_headers,
                    timeout=30  # 设置超时时间为30秒
                )
                
                # 检查响应状态码
                response.raise_for_status()
                
                # 解析响应数据
                result = response.json()
                
                # 对于GET请求，缓存结果
                if use_cache and method.upper() == 'GET':
                    self._save_to_cache(endpoint, result, params)
                    
                logger.info(f"API调用成功: {endpoint}")
                return result
                
            except RequestException as e:
                last_error = e
                logger.warning(f"API调用失败: {endpoint}, 尝试 {attempt+1}/{retries}, 错误: {str(e)}")
                
                if attempt < retries - 1:
                    time.sleep(self.retry_delay * (2 ** attempt))  # 指数级退避
                    
        # 所有重试都失败了
        error_msg = str(last_error) if last_error else "未知错误"
        logger.error(f"API调用完全失败: {endpoint}, 错误: {error_msg}")
        return {"error": error_msg, "success": False}
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        发送GET请求
        
        Args:
            endpoint: API接口路径
            params: URL参数
            **kwargs: 其他参数
            
        Returns:
            API响应数据
        """
        return self.call_api(endpoint, 'GET', params=params, **kwargs)
        
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        发送POST请求
        
        Args:
            endpoint: API接口路径
            data: 请求数据
            **kwargs: 其他参数
            
        Returns:
            API响应数据
        """
        return self.call_api(endpoint, 'POST', data=data, **kwargs)
        
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        发送PUT请求
        
        Args:
            endpoint: API接口路径
            data: 请求数据
            **kwargs: 其他参数
            
        Returns:
            API响应数据
        """
        return self.call_api(endpoint, 'PUT', data=data, **kwargs)
        
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        发送DELETE请求
        
        Args:
            endpoint: API接口路径
            **kwargs: 其他参数
            
        Returns:
            API响应数据
        """
        return self.call_api(endpoint, 'DELETE', **kwargs)
        
    def _get_cache_key(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        生成缓存键
        
        Args:
            endpoint: API接口路径
            params: URL参数
            
        Returns:
            缓存键
        """
        params_str = json.dumps(params or {}, sort_keys=True)
        import hashlib
        cache_key = hashlib.md5(f"{endpoint}:{params_str}".encode()).hexdigest()
        return cache_key
        
    def _get_from_cache(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        从缓存获取数据
        
        Args:
            endpoint: API接口路径
            params: URL参数
            
        Returns:
            缓存的数据，如果未命中缓存则返回None
        """
        cache_key = self._get_cache_key(endpoint, params)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if not os.path.exists(cache_file):
            return None
            
        # 检查缓存是否过期
        cache_time = os.path.getmtime(cache_file)
        if time.time() - cache_time > self.cache_expiration:
            logger.debug(f"缓存已过期: {endpoint}")
            return None
            
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                logger.debug(f"缓存命中: {endpoint}")
                return cache_data
        except Exception as e:
            logger.warning(f"读取缓存失败: {endpoint}, 错误: {str(e)}")
            return None
            
    def _save_to_cache(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> bool:
        """
        保存数据到缓存
        
        Args:
            endpoint: API接口路径
            data: 要缓存的数据
            params: URL参数
            
        Returns:
            保存是否成功
        """
        try:
            cache_key = self._get_cache_key(endpoint, params)
            cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            logger.debug(f"数据已缓存: {endpoint}")
            return True
            
        except Exception as e:
            logger.warning(f"缓存数据失败: {endpoint}, 错误: {str(e)}")
            return False
            
    def clear_cache(self, endpoint: Optional[str] = None, params: Optional[Dict[str, Any]] = None) -> int:
        """
        清除缓存
        
        Args:
            endpoint: API接口路径，如果为None则清除所有缓存
            params: URL参数，如果endpoint不为None且params为None则清除该接口的所有缓存
            
        Returns:
            清除的缓存文件数量
        """
        cleared_count = 0
        
        if endpoint is not None:
            if params is not None:
                # 清除特定接口和参数的缓存
                cache_key = self._get_cache_key(endpoint, params)
                cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
                
                if os.path.exists(cache_file):
                    os.remove(cache_file)
                    cleared_count = 1
                    logger.info(f"已清除接口缓存: {endpoint}")
            else:
                # 清除特定接口的所有缓存（前缀匹配）
                endpoint_encoded = endpoint.replace('/', '_')
                
                for filename in os.listdir(self.cache_dir):
                    if filename.startswith(endpoint_encoded) and filename.endswith('.json'):
                        os.remove(os.path.join(self.cache_dir, filename))
                        cleared_count += 1
                        
                logger.info(f"已清除接口相关的所有缓存: {endpoint}, 共 {cleared_count} 个文件")
        else:
            # 清除所有缓存
            if os.path.exists(self.cache_dir):
                for filename in os.listdir(self.cache_dir):
                    if filename.endswith('.json'):
                        os.remove(os.path.join(self.cache_dir, filename))
                        cleared_count += 1
                        
                logger.info(f"已清除所有缓存，共 {cleared_count} 个文件")
                
        return cleared_count
        
    def set_api_key(self, api_key: str) -> None:
        """
        设置API密钥
        
        Args:
            api_key: API密钥
        """
        self.api_key = api_key
        self.headers['Authorization'] = f'Bearer {self.api_key}'
        logger.info("已更新API密钥")
        
    def set_base_url(self, base_url: str) -> None:
        """
        设置API基础URL
        
        Args:
            base_url: API基础URL
        """
        self.base_url = base_url
        logger.info(f"已更新API基础URL: {base_url[:30]}{'...' if len(base_url) > 30 else ''}")
        
    def check_connectivity(self) -> bool:
        """
        检查API连接性
        
        Returns:
            连接是否成功
        """
        if not self.base_url:
            logger.error("未设置API基础URL，无法检查连接性")
            return False
            
        try:
            # 尝试访问根路径或健康检查路径
            response = requests.get(
                url=f"{self.base_url.rstrip('/')}/health",
                headers=self.headers,
                timeout=5
            )
            
            if response.status_code == 404:
                # 如果健康检查路径不存在，尝试根路径
                response = requests.get(
                    url=self.base_url.rstrip('/'),
                    headers=self.headers,
                    timeout=5
                )
                
            # 检查响应状态码
            if response.status_code < 400:
                logger.info("API连接正常")
                return True
            else:
                logger.warning(f"API连接失败，状态码: {response.status_code}")
                return False
                
        except RequestException as e:
            logger.error(f"API连接失败: {str(e)}")
            return False
            
    def register_mock_service(self, service: 'MockDataService') -> None:
        """
        注册模拟数据服务
        
        Args:
            service: 模拟数据服务实例
        """
        self.mock_service = service
        logger.info("已注册模拟数据服务")
        
    def use_mock(self, mock_enabled: bool = True) -> None:
        """
        设置是否使用模拟数据
        
        Args:
            mock_enabled: 是否启用模拟数据
        """
        self.mock_enabled = mock_enabled
        logger.info(f"{'启用' if mock_enabled else '禁用'}模拟数据")
        
    def call_with_mock(self, endpoint: str, method: str = 'GET',
                      params: Optional[Dict[str, Any]] = None,
                      data: Optional[Dict[str, Any]] = None,
                      **kwargs) -> Dict[str, Any]:
        """
        调用API接口，支持模拟数据
        
        Args:
            endpoint: API接口路径
            method: 请求方法
            params: URL参数
            data: 请求数据
            **kwargs: 其他参数
            
        Returns:
            API响应数据，出错时返回包含错误信息的字典
        """
        # 检查是否应该使用模拟数据
        if hasattr(self, 'mock_enabled') and self.mock_enabled and hasattr(self, 'mock_service'):
            mock_result = self.mock_service.get_mock_data(endpoint, method, params, data)
            if mock_result is not None:
                logger.info(f"使用模拟数据: {endpoint}")
                # 添加一些模拟的网络延迟，使其更真实
                time.sleep(0.1)
                return mock_result
                
        # 如果不使用模拟数据或没有匹配的模拟数据，使用真实API调用
        return self.call_api(endpoint, method, params, data, **kwargs)
        
    def get_with_mock(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        发送GET请求，支持模拟数据
        
        Args:
            endpoint: API接口路径
            params: URL参数
            **kwargs: 其他参数
            
        Returns:
            API响应数据
        """
        return self.call_with_mock(endpoint, 'GET', params=params, **kwargs)
        
    def post_with_mock(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        发送POST请求，支持模拟数据
        
        Args:
            endpoint: API接口路径
            data: 请求数据
            **kwargs: 其他参数
            
        Returns:
            API响应数据
        """
        return self.call_with_mock(endpoint, 'POST', data=data, **kwargs)
