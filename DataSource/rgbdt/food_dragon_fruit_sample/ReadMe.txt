RGBDT データセット

製作者 : moriitkys@ROBOTAiM

----- 202102 -----

[LICENSE]
・このデータの利用により生じた問題には製作者は一切責任を負いません。
・このデータの著作権は全て製作者に帰属します。
・製作者が宣言しない限りこのデータの著作権を放棄することはありません。
・返金は受け付けていません。sampleデータを確認したうえで購入をよく検討してください。
・このデータを用いた場合、参考や謝辞などで製作者（moriitkys）の表記を可能な限り実施してください。

・ The creator is not responsible for any problems caused by the use of this data.
・ All copyrights of this data belong to the creator. -Unless the creator declares, I will not waive the copyright of this data.
・ Refunds are not accepted. Please consider purchasing after checking the sample data.
・ When using this data, please use the notation of the creator (moriitkys) as much as possible for reference and acknowledgments.

禁止事項 Prohibited matter
・このデータの再配布や無断転載は厳禁です。
・このデータを用いて作成された改変データなどの配布・販売などは禁止します。
・政治、宗教活動、他者に対する誹謗中傷目的での使用、違法行為への利用を禁止します。
・このデータの製作者であると主張することを禁止します。

・ It is strictly prohibited to redistribute or reprint this data without permission.
・ Distribution and sale of modified data created using this data is prohibited.
・ Political and religious activities, use for the purpose of slander against others, and use for illegal acts are prohibited.
・ It is prohibited to claim to be the creator of this data.

可能事項 Possible matters
・学術目的、研究目的での利用は可能です。
・組織内での共有は可能です。
・このデータを機械学習などで学習して得られた結果を用いたアプリケーションなどの配布や販売は可能です。ただし、このデータの形式を保ったままパッケージに含めて配布するようなことは禁止します。

・ It can be used for academic and research purposes.
・ Sharing within the organization is possible.
・ It is possible to distribute and sell applications created by using this data for machine learning etc. However, it is prohibited to distribute this data in a package while maintaining the format of this data.

[About GT(Ground Truth)]
申し訳ありません。"industrial"データについては基本的に温度データをとっていません。表面温度は環境温度と顕著な差が無いためです。
ただし、環境温度としては25~28度程度の屋内で撮影しています。温度はthermal_rawデータをもとに算出してください。
今後、温度生データからセルシウス温度を計算するためのデータセットや式を提供する可能性はあります。
I'm sorry. Basically, the thermal data is not taken for "industrial" data. This is because the surface temperature is not significantly different from the environmental temperature.
However, the environmental temperature is about 25 to 28 degrees indoors. Calculate the temperature based on the raw thermal data.
In the future, we may provide datasets and formulas for calculating Celsius temperature from raw thermal data.

現時点では"形状GT"と"オブジェクト温度GT"については以下のようになっています。
food : 形状GTなし、 オブジェクト温度GTあり
industrial : 形状GTあり、 オブジェクト温度GTなし

At the moment, the "Shape GT" and "object thermal GT" are as follows.
food : Shape GT Available, Object thermal GT None
industrial : Shape GT None, Object thermal GT Available


[About Thermal Data from Seek Thermal and aimedata (TOAMIT)]
画像データの取得にはSeek Thermalを用いています。
GTの取得には「TOAMIT 東亜産業 非接触式電子温度計 アイメディータ aimedata」を用いています。
GTは信頼性が低いです。Seek Thermalについても精度は期待できません。
Seek Thermal is used to acquire image data.
"aimedata (TOAMIT)" is used to acquire GT.
GT is unreliable. Seek Thermal is also unreliable.

温度データcsvはSeek Thermalの生データで構成されている（簡易的な式は以下）
The thermal data(csv) consists of raw thermal data from Seek Thermal (simple formula is below)
t [degree C] = t_raw * 0.0155236856 - 214.77236
注意　線形補間かつ私のセンサでの式なので注意。常温付近で少し低く測定される（？）
Note that it is a linear interpolation and the formula with my sensor. Measured slightly lower near room temperature (?)

注意　高温（約30℃以上）のものは時間経過とともに温度が下がってくるため、温度は一定ではありません。水分を含む低温のものであっても、時間経過とともに温度変化する場合があるので、ご注意ください。
The temperature of hot objects is not constant throughout the whole data because the temperature drops. Even low temperatures that contain moisture may change in temperature throughout the whole data.