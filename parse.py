import re
import requests
import json
import time
import asyncio
# phản hồi từ api
def decode_unicode(text):
    return re.sub(r'\\u[\dA-F]{4}', lambda match: chr(int(match.group(0)[2:], 16)), text)

async def sendMessage(question, chat_id, token):
    try:
        api_url = "https://api.chatx.vn/v1/chat-messages"
        user_ip = "testparse"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        data = {
            "inputs": {},
            "query": question,
            "response_mode": "streaming",
            "conversation_id": chat_id,
            "user": user_ip
        }

        response = requests.post(api_url, headers=headers, data=json.dumps(data), stream=True)

        if not response.ok:
            raise Exception(f"HTTP error! status: {response.status_code}")

        result = ""
        conversation_id = ""
        buffer = ""
        message_end_received = False

        for line in response.iter_lines():
            if line:
                line_str = line.decode("utf-8")
                buffer += line_str
                if line_str.startswith("data: "):
                    try:
                        data = json.loads(line_str[6:])
                        if data["event"] == "agent_message":
                            result += decode_unicode(data["answer"])
                        elif data["event"] == "message_end":
                            conversation_id = data["conversation_id"]
                            message_end_received = True
                    except json.JSONDecodeError:
                        print("Error parsing JSON:", line_str)

                if message_end_received:
                    break

        # Wait for an additional short period of time to ensure all data is received
        if message_end_received:
            time.sleep(1)
        
        answer = result.strip()
        # print(answer)
        return {"answer": answer}
    except Exception as e:
        print("Error in send_message_to_agent_v2:", e)
        raise Exception("Cannot send message to agent")

# getMessage()
async def main():
    data = await sendMessage("a cao m7 nặng 60kg thì có bộ nào k", "bfc3dd2e-3f10-43a1-8302-62a703204920", "app-aa7eQZDrHSiz9U5KLKepTBxb")
    regex = r"\[(.*?)\]\((.*?)\)"
    # Tách đoạn văn thành mảng với mỗi phần từ là text sau khi xuống dòng "\n"  
    res_array = data["answer"].split('\n')

    result = []
    # Lặp quanh mảng nếu có mảng nào phù hợp với regex thì lấy ra link ảnh 
    for item in res_array:
        match = re.search(regex, item)
        if match:
            # in ra link ảnh sau khi xử lý được link
            result.append(match.group(2))
            # print(match.group(2))
        else:
            # nếu không phù hợp với regex thì chỉ in
            result.append(item)
            # print(item)    
    for item in result:
        time.sleep(1)
        print(item)



    
if __name__ == "__main__":
    asyncio.run(main())

