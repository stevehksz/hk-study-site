# -*- coding: utf-8 -*-
"""朗文 LWTE GOLD 5A/5B Word Bank 詞庫 → _lwte_vocab.json
提取方式：Word Bank .doc（piece table 解析，build_lwte.py 舊版已驗證），兩欄排版串行已人工清理。
版權性質：詞條為教材詞庫頁的常見短語/單詞列表（事實性內容），中文釋義為自譯；版權屬 Pearson，站內標注僅供家庭學習。
"""
import json, os

A = {
 'Actions': [('bath the baby','給嬰兒洗澡'),('dress the baby','給嬰兒穿衣'),('feed the baby','餵嬰兒'),
  ('read stories to the baby','給嬰兒講故事'),('share my toys with the baby','和嬰兒分享玩具'),
  ('take photos of the baby','給嬰兒拍照'),('take the baby for a walk','帶嬰兒散步'),('teach the baby rhymes','教嬰兒念童謠')],
 'Plans': [('go swimming','去游泳'),('join the Art Club','加入美術社'),('join the Storytelling Club','加入故事社'),
  ('play sport','做運動'),('read English books','讀英文書'),('study hard','努力學習'),('take a Japanese course','上日語課')],
 'Activities': [('fly kites','放風箏'),('go on a picnic','去野餐'),('go skating','去溜冰'),
  ('sing karaoke','唱卡拉OK'),('watch a film','看電影')],
 'Illnesses': [('a broken arm','手臂骨折'),('a cold','感冒'),('a cough','咳嗽'),('a fever','發燒'),
  ('a headache','頭痛'),('a sore throat','喉嚨痛'),('a stomachache','肚子痛'),('a toothache','牙痛')],
 'Things to do when you are ill': [('drink more water','多喝水'),('eat more fruit','多吃水果'),
  ('get an X-ray','拍 X 光'),('rest in bed','臥床休息'),('take some medicine','吃藥')],
 'Weather': [('foggy','有霧的'),('wet','潮濕的'),('windy','有風的')],
 'Things around us': [('a comb','梳子'),('a comic','漫畫書'),('an envelope','信封'),('a handkerchief','手帕'),
  ('a hole punch','打孔機'),('a magazine','雜誌'),('a mirror','鏡子'),('a newspaper','報紙'),
  ('a pair of scissors','一把剪刀'),('a pin','大頭針'),('some soap','一些肥皂'),('a stapler','釘書機'),
  ('a swimsuit','泳衣'),('a table tennis bat','乒乓球拍'),('some tissues','一些紙巾'),('some toothpaste','一些牙膏'),
  ('a toothbrush','牙刷'),('a towel','毛巾'),('an umbrella','雨傘'),('a watch','手錶')],
 'Festivals and activities': [('get red packets','收紅包'),('wear new clothes','穿新衣'),
  ('eat rice dumplings','吃糉子'),('watch dragon boat races','看龍舟賽'),('eat moon cakes','吃月餅'),
  ('play with lanterns','玩燈籠'),('guess riddles','猜燈謎'),('eat sweet dumplings','吃湯圓'),
  ('go hiking','去遠足'),('decorate the Christmas tree','裝飾聖誕樹'),('give presents','送禮物'),
  ('send Christmas cards','寄聖誕卡'),('wear a costume','穿化裝服飾'),('give flowers to my mother','送花給媽媽')],
}
B = {
 'Actions (1)': [('draw a sign','畫告示牌'),('write a notice','寫通知'),('paint a fence','油漆柵欄'),
  ('break a flowerpot','打破花盆'),('make the bed','整理床鋪'),('tidy the room','收拾房間'),
  ('throw away the rubbish','丟垃圾'),('sweep the floor','掃地'),('do the washing','洗衣服'),
  ('put the tables and chairs away','收好桌椅'),('drive a racing car','駕駛賽車'),('fly a helicopter','開直升機'),
  ('meet a famous person','與名人會面'),('participate in a charity walk','參加慈善步行'),('watch a parade','看遊行'),
  ('see a pop concert','看流行演唱會'),('perform in a Peking opera','表演京劇'),('plant trees on National Tree-planting Day','植樹節種樹'),
  ('have snake soup','喝蛇湯'),('give flowers to a pop star','送花給明星')],
 'Actions (2)': [('celebrate Halloween','慶祝萬聖節'),('eat insects','吃昆蟲'),('pick fruit','摘水果'),
  ('watch birds','觀鳥'),('go fishing','去釣魚'),('look at plants and flowers','觀察花草'),
  ('go horse-riding','去騎馬'),('watch wild animals','看野生動物'),('watch butterflies','看蝴蝶'),('go hiking','去遠足')],
 'Animals': [('a sea turtle','海龜'),('an Asian elephant','亞洲象'),('a black-faced spoonbill','黑面琵鷺'),
  ('an orang-utan','紅毛猩猩'),('a Chinese white dolphin','中華白海豚')],
 'Feelings': [('shocked','震驚的'),('tired','疲倦的'),('frightened','害怕的'),('surprised','驚訝的')],
 'Meat': [('chicken','雞肉'),('pork','豬肉'),('beef','牛肉'),('sausages','香腸'),('duck','鴨肉')],
 'Vegetables': [('peas','豌豆'),('broccoli','西蘭花'),('lettuce','生菜'),('sweet corn','粟米')],
 'Fruit': [('grapes','葡萄')],
 'Snacks': [('a fruit tart','水果撻'),('ice cream','雪糕'),('yoghurt','乳酪'),('crackers','克力架餅'),
  ('potato chips','薯片'),('chocolate','朱古力'),('cookies','曲奇')],
 'Drink': [('apple juice','蘋果汁'),('milk','牛奶'),('tea','茶')],
 'Seafood': [('fish','魚')],
 'Others': [('bread','麵包'),('spaghetti','意大利麵'),('noodles','麵'),('rice','米飯'),
  ('a chicken wing','雞翼'),('dim sum','點心'),('hot dog','熱狗'),('a steamed bun','包子'),
  ('butter','牛油'),('salad dressing','沙拉醬')],
}
out = []
for bk, d in (('5A', A), ('5B', B)):
    for cat, items in d.items():
        out.append({'bk': bk, 'cat': cat, 'items': [{'w': w, 'zh': z} for w, z in items]})
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lwte_vocab.json')
json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
n = sum(len(e['items']) for e in out)
print(f'朗文詞庫：{len(out)} 類 {n} 條（5A {sum(len(e["items"]) for e in out if e["bk"]=="5A")} / 5B {sum(len(e["items"]) for e in out if e["bk"]=="5B")}）')
