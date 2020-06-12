package com.fine.data;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class Portfolio {
    public PortfolioValue value = new PortfolioValue();
    public List<StockItem> stocks = new ArrayList<>();
    public List<Float> day = new ArrayList<>();
    public List<Float> week;
    public List<Float> month;
    public List<Float> ytd = new ArrayList<>();

    public Portfolio fromJSON(JSONObject json) {
        PortfolioValue value = new PortfolioValue();
        this.value = value.fromJSON(json.optJSONObject("value"));
        JSONArray stocksJson = json.optJSONArray("stocks");
        if (stocksJson != null) {
            List<StockItem> stocks = new ArrayList<>();
            for (int i = 0; i < stocksJson.length(); i++) {
                StockItem stockItem = new StockItem();
                stocks.add(stockItem.fromJSON(stocksJson.optJSONObject(i)));
            }
            this.stocks = stocks;
        }
        JSONObject timeSeries = json.optJSONObject("time_series");
        if (timeSeries != null) {
            JSONObject day = timeSeries.optJSONObject("1d");
            JSONObject week = timeSeries.optJSONObject("1w");
            JSONObject month = timeSeries.optJSONObject("1m");
            JSONObject ytd = timeSeries.optJSONObject("ytd");
            this.day = getVallues(day);
            this.week = getVallues(week);
            this.month = getVallues(month);
            this.ytd = getVallues(ytd);
        }
        return this;
    }

    public List<Float> getVallues(JSONObject json) {
        Iterator<String> keys = json.keys();
        List<Float> listValues = new ArrayList<>();
        while (keys.hasNext()) {
            listValues.add((float) json.optDouble(keys.next()));
        }
        return listValues;
    }

    public class PortfolioValue {
        public double close;
        public double open;
        public double jump;
        public boolean isNegative;

        public PortfolioValue fromJSON(JSONObject json) {
            this.close = json.optDouble("close");
            this.open = json.optDouble("open");
            this.isNegative = !isPositive(this.open, this.close);
            this.jump = this.close / this.open - 1;
            return this;
        }
    }

    public class StockItem {
        public String symbol;
        public double percent;
        public double close;
        public double open;
        public double jump;
        public boolean isPositive;

        public StockItem fromJSON(JSONObject json) {
            this.symbol = json.optString("symbol");
            this.percent = json.optDouble("percent");
            this.close = json.optDouble("close");
            this.open = json.optDouble("open");
            this.isPositive = isPositive(this.open, this.close);
            this.jump = this.close / this.open - 1;
            return this;
        }
    }

    private boolean isPositive(double open, double close) {
        return close - open >= 0;
    }
}