import google.generativeai as genai
import json
import requests

def web_search(query):
    """使用 DuckDuckGo 搜尋 API 取得前幾筆結果"""
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1,
    }
    response = requests.get(url, params=params)
    data = response.json()
    results = []
    
    if "RelatedTopics" in data:
        for item in data["RelatedTopics"][:5]:
            if "Text" in item and "FirstURL" in item:
                results.append({
                    "title": item["Text"],
                    "url": item["FirstURL"]
                })
    return results


genai.configure(api_key="AIzaSyCIsLvPKLi9abhh6k3I9ZWFbHhSXww3j_w")
model = genai.GenerativeModel("gemini-2.5-flash")


def 主程式(question):
    詢問gemnine需要搜尋嗎 = model.generate_content(f"問題:{question}。請回答：是否需要查詢網路才能回答？只回答 是 或 否。")
    x= "是" in 詢問gemnine需要搜尋嗎.text #是否需要查詢網路，是的話x設為true，不是的話x設為false

    if x:   # 需要搜尋(即true)，問DuckDuckGo(用web_search)
        print("需要搜尋中")
        results = web_search(question)
        if results:
            summary_text = "\n".join([f"{r['title']} ({r['url']})" for r in results])
            full_prompt = f"使用以下資料回答問題：\n{summary_text}\n\n問題：{question}\n請產生一個清晰簡潔的回答。"
            answer = model.generate_content(full_prompt)
            return answer.text
        else:
            return "查不到相關資料。"
    
    else:  # 不需要搜尋，直接回答
        answer = model.generate_content(question)
        return answer.text





if __name__ == "__main__":
    while True:
        question = input("\n 請輸入問題（或輸入 'exit' 離開）：")
        if question.lower() == "exit":
            break
        print("\n 機器人回答：", 主程式(question))
