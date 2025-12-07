"""Unit tests for tool calls and reasoning support."""

import unittest
from unittest.mock import patch, Mock
import json
from pollinations import Pollinations


class TestToolCalls(unittest.TestCase):
    """Test cases for tool calls functionality."""
    
    def setUp(self):
        """Set up test client."""
        self.client = Pollinations(timeout=30)
    
    @patch('pollinations.openai_compat.requests.post')
    def test_chat_with_tools_parameter(self, mock_post):
        """Test that tools parameter is passed to API."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "id": "chatcmpl-test",
            "object": "chat.completion",
            "created": 1234567890,
            "model": "openai",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "I will use the get_weather tool."
                },
                "finish_reason": "stop"
            }]
        }
        mock_post.return_value = mock_response
        
        tools = [{
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City name"
                        }
                    }
                }
            }
        }]
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": "What's the weather?"}],
            tools=tools
        )
        
        # Verify tools were passed in the request
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        self.assertIn('tools', payload)
        self.assertEqual(payload['tools'], tools)
        self.assertIsNotNone(response)
    
    @patch('pollinations.openai_compat.requests.post')
    def test_chat_with_tool_choice_parameter(self, mock_post):
        """Test that tool_choice parameter is passed to API."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "id": "chatcmpl-test",
            "object": "chat.completion",
            "model": "openai",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": "call_123",
                        "type": "function",
                        "function": {
                            "name": "get_weather",
                            "arguments": '{"location": "London"}'
                        }
                    }]
                },
                "finish_reason": "tool_calls"
            }]
        }
        mock_post.return_value = mock_response
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": "Weather in London?"}],
            tools=[{
                "type": "function",
                "function": {"name": "get_weather"}
            }],
            tool_choice={"type": "function", "function": {"name": "get_weather"}}
        )
        
        # Verify tool_choice was passed
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        self.assertIn('tool_choice', payload)
        self.assertEqual(response.choices[0].finish_reason, "tool_calls")
    
    @patch('pollinations.openai_compat.requests.post')
    def test_response_with_tool_calls(self, mock_post):
        """Test parsing response with tool calls."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "id": "chatcmpl-test",
            "object": "chat.completion",
            "model": "openai",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": "call_abc123",
                        "type": "function",
                        "function": {
                            "name": "get_weather",
                            "arguments": '{"location": "San Francisco", "unit": "celsius"}'
                        }
                    }]
                },
                "finish_reason": "tool_calls"
            }]
        }
        mock_post.return_value = mock_response
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": "Weather in SF?"}],
            tools=[{"type": "function", "function": {"name": "get_weather"}}]
        )
        
        # Verify tool calls are parsed correctly
        self.assertIsNotNone(response.choices[0].message.tool_calls)
        self.assertEqual(len(response.choices[0].message.tool_calls), 1)
        tool_call = response.choices[0].message.tool_calls[0]
        self.assertEqual(tool_call.id, "call_abc123")
        self.assertEqual(tool_call.type, "function")
        self.assertEqual(tool_call.function.name, "get_weather")
        self.assertEqual(tool_call.function.arguments, '{"location": "San Francisco", "unit": "celsius"}')
    
    @patch('pollinations.openai_compat.requests.post')
    def test_response_with_multiple_tool_calls(self, mock_post):
        """Test parsing response with multiple tool calls."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "id": "chatcmpl-test",
            "object": "chat.completion",
            "model": "openai",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "call_1",
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "arguments": '{"location": "NYC"}'
                            }
                        },
                        {
                            "id": "call_2",
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "arguments": '{"location": "LA"}'
                            }
                        }
                    ]
                },
                "finish_reason": "tool_calls"
            }]
        }
        mock_post.return_value = mock_response
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": "Weather in NYC and LA?"}],
            tools=[{"type": "function", "function": {"name": "get_weather"}}]
        )
        
        # Verify multiple tool calls are parsed
        self.assertEqual(len(response.choices[0].message.tool_calls), 2)
        self.assertEqual(response.choices[0].message.tool_calls[0].function.name, "get_weather")
        self.assertEqual(response.choices[0].message.tool_calls[1].function.name, "get_weather")
    
    @patch('pollinations.openai_compat.requests.post')
    def test_streaming_with_tool_calls(self, mock_post):
        """Test streaming response with tool calls."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        
        # Mock streaming data with tool calls
        stream_data = [
            b'data: {"choices":[{"delta":{"role":"assistant","tool_calls":[{"id":"call_1","type":"function","function":{"name":"get_weather","arguments":""}}]},"finish_reason":null}]}',
            b'data: {"choices":[{"delta":{"tool_calls":[{"function":{"arguments":"{\\"location\\""}}]},"finish_reason":null}]}',
            b'data: {"choices":[{"delta":{"tool_calls":[{"function":{"arguments":": \\"NYC\\"}"}}]},"finish_reason":null}]}',
            b'data: {"choices":[{"delta":{},"finish_reason":"tool_calls"}]}',
        ]
        
        mock_response.iter_lines.return_value = stream_data
        mock_post.return_value = mock_response
        
        stream = self.client.chat.completions.create(
            messages=[{"role": "user", "content": "Weather in NYC?"}],
            tools=[{"type": "function", "function": {"name": "get_weather"}}],
            stream=True
        )
        
        chunks = list(stream)
        
        # Verify we got chunks
        self.assertGreater(len(chunks), 0)
        
        # Verify first chunk has tool_calls delta
        first_chunk = chunks[0]
        self.assertIsNotNone(first_chunk.choices[0].delta.tool_calls)


class TestReasoning(unittest.TestCase):
    """Test cases for reasoning functionality."""
    
    def setUp(self):
        """Set up test client."""
        self.client = Pollinations(timeout=30)
    
    @patch('pollinations.openai_compat.requests.post')
    def test_chat_with_reasoning_effort(self, mock_post):
        """Test that reasoning_effort parameter is passed to API."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "id": "chatcmpl-test",
            "object": "chat.completion",
            "model": "openai",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "The answer is 42.",
                    "reasoning_content": "Let me think step by step..."
                },
                "finish_reason": "stop"
            }]
        }
        mock_post.return_value = mock_response
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": "Solve this problem"}],
            reasoning_effort="high"
        )
        
        # Verify reasoning_effort was passed
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        self.assertIn('reasoning_effort', payload)
        self.assertEqual(payload['reasoning_effort'], "high")
    
    @patch('pollinations.openai_compat.requests.post')
    def test_response_with_reasoning_content(self, mock_post):
        """Test parsing response with reasoning content."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "id": "chatcmpl-test",
            "object": "chat.completion",
            "model": "openai",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "The answer is 42.",
                    "reasoning_content": "First, I need to analyze the question. The ultimate answer to life, the universe, and everything is known from the Hitchhiker's Guide to be 42."
                },
                "finish_reason": "stop"
            }]
        }
        mock_post.return_value = mock_response
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": "What is the ultimate answer?"}],
            reasoning_effort="medium"
        )
        
        # Verify reasoning content is parsed
        self.assertIsNotNone(response.choices[0].message.reasoning_content)
        self.assertIn("analyze", response.choices[0].message.reasoning_content)
        self.assertEqual(response.choices[0].message.content, "The answer is 42.")
    
    @patch('pollinations.openai_compat.requests.post')
    def test_streaming_with_reasoning(self, mock_post):
        """Test streaming response with reasoning content."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        
        stream_data = [
            b'data: {"choices":[{"delta":{"role":"assistant","reasoning_content":"Let me think"},"finish_reason":null}]}',
            b'data: {"choices":[{"delta":{"reasoning_content":" step by step..."},"finish_reason":null}]}',
            b'data: {"choices":[{"delta":{"content":"The answer"},"finish_reason":null}]}',
            b'data: {"choices":[{"delta":{"content":" is 42."},"finish_reason":null}]}',
            b'data: {"choices":[{"delta":{},"finish_reason":"stop"}]}',
        ]
        
        mock_response.iter_lines.return_value = stream_data
        mock_post.return_value = mock_response
        
        stream = self.client.chat.completions.create(
            messages=[{"role": "user", "content": "Solve this"}],
            reasoning_effort="high",
            stream=True
        )
        
        chunks = list(stream)
        
        # Verify we got chunks
        self.assertGreater(len(chunks), 0)
        
        # Collect reasoning and content separately
        reasoning_parts = []
        content_parts = []
        for chunk in chunks:
            if chunk.choices[0].delta.reasoning_content:
                reasoning_parts.append(chunk.choices[0].delta.reasoning_content)
            if chunk.choices[0].delta.content:
                content_parts.append(chunk.choices[0].delta.content)
        
        # Verify we got both reasoning and content
        self.assertGreater(len(reasoning_parts), 0)
        self.assertGreater(len(content_parts), 0)
    
    @patch('pollinations.openai_compat.requests.post')
    def test_reasoning_effort_values(self, mock_post):
        """Test different reasoning_effort values."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "choices": [{
                "message": {"role": "assistant", "content": "Answer"},
                "finish_reason": "stop"
            }]
        }
        mock_post.return_value = mock_response
        
        for effort in ["low", "medium", "high"]:
            self.client.chat.completions.create(
                messages=[{"role": "user", "content": "Test"}],
                reasoning_effort=effort
            )
            
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            self.assertEqual(payload['reasoning_effort'], effort)


class TestToolCallsAndReasoningIntegration(unittest.TestCase):
    """Test cases for combined tool calls and reasoning."""
    
    def setUp(self):
        """Set up test client."""
        self.client = Pollinations(timeout=30)
    
    @patch('pollinations.openai_compat.requests.post')
    def test_tool_calls_with_reasoning(self, mock_post):
        """Test response with both tool calls and reasoning content."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "id": "chatcmpl-test",
            "object": "chat.completion",
            "model": "openai",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": None,
                    "reasoning_content": "I need to check the weather to answer this question.",
                    "tool_calls": [{
                        "id": "call_123",
                        "type": "function",
                        "function": {
                            "name": "get_weather",
                            "arguments": '{"location": "Paris"}'
                        }
                    }]
                },
                "finish_reason": "tool_calls"
            }]
        }
        mock_post.return_value = mock_response
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": "Should I bring an umbrella in Paris?"}],
            tools=[{"type": "function", "function": {"name": "get_weather"}}],
            reasoning_effort="medium"
        )
        
        # Verify both reasoning and tool calls are present
        self.assertIsNotNone(response.choices[0].message.reasoning_content)
        self.assertIsNotNone(response.choices[0].message.tool_calls)
        self.assertIn("weather", response.choices[0].message.reasoning_content.lower())
    
    @patch('pollinations.openai_compat.requests.post')
    def test_message_to_dict_with_all_fields(self, mock_post):
        """Test that ChatCompletionMessage.to_dict() includes all fields."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "Answer",
                    "reasoning_content": "Reasoning",
                    "tool_calls": [{
                        "id": "call_1",
                        "type": "function",
                        "function": {"name": "test", "arguments": "{}"}
                    }]
                },
                "finish_reason": "tool_calls"
            }]
        }
        mock_post.return_value = mock_response
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": "Test"}]
        )
        
        message_dict = response.choices[0].message.to_dict()
        
        # Verify all fields are in the dict
        self.assertIn("role", message_dict)
        self.assertIn("content", message_dict)
        self.assertIn("reasoning_content", message_dict)
        self.assertIn("tool_calls", message_dict)


if __name__ == '__main__':
    unittest.main()
