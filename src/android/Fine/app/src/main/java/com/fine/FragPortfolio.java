package com.fine;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ListView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;

import com.fine.data.Portfolio;
import com.robinhood.spark.SparkAdapter;
import com.robinhood.spark.SparkView;

import java.util.ArrayList;
import java.util.List;

import static com.fine.FineApp.app;

public class FragPortfolio extends Fragment {

    static final String SELECTED_SYMBOL = "selected_symbol";
    static final String BID_VALUE = "bid_value";
    private TextView selectedPeriodTextView;
    private boolean showPrice = true;
    private String selected;
    private double bidValue;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        app().downloadPortfolio();

        if (getArguments() != null) {
            selected = getArguments().getString(SELECTED_SYMBOL);
            bidValue = getArguments().getDouble(BID_VALUE);
            setArguments(null);
        }

        View rootView = inflater.inflate(R.layout.frag_portfolio, container, false);
        final ListView listView = rootView.findViewById(R.id.frag_portfolio_list);
        View vgGraph = inflater.inflate(R.layout.convert_portfolio_graph, listView, false);
        View vgValue = inflater.inflate(R.layout.convert_portfolio_value, listView, false);
        SparkView sparkView = vgGraph.findViewById(R.id.convert_portfolio_graph_sparkview);
        final TextView txtScrubInfo = vgGraph.findViewById(R.id.convert_portfolio_graph_txt_scrub_info);
        final TextView btnDay = vgGraph.findViewById(R.id.convert_portfolio_graph_btn_day);
        final TextView btnWeek = vgGraph.findViewById(R.id.convert_portfolio_graph_btn_week);
        final TextView btnMonth = vgGraph.findViewById(R.id.convert_portfolio_graph_btn_month);
        final TextView btnYtd = vgGraph.findViewById(R.id.convert_portfolio_graph_btn_ytd);
        final TextView txtValue = vgValue.findViewById(R.id.convert_portfolio_value_txt);

        final FineSparkAdapter sparkAdapter = new FineSparkAdapter();

        btnDay.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                selectedPeriodTextView.setBackgroundResource(android.R.color.transparent);
                selectedPeriodTextView.setTextColor(getResources().getColor(R.color.orange));
                selectedPeriodTextView = btnDay;
                btnDay.setTextColor(getResources().getColor(R.color.white));
                view.setBackground(getResources().getDrawable(R.drawable.rounded_corner));
                sparkAdapter.setPeriod(app().getState().getPortfolioMutableLiveData().getValue().day);
            }
        });

        btnMonth.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                selectedPeriodTextView.setBackgroundResource(android.R.color.transparent);
                selectedPeriodTextView.setTextColor(getResources().getColor(R.color.orange));
                selectedPeriodTextView = btnMonth;
                btnMonth.setTextColor(getResources().getColor(R.color.white));
                view.setBackground(getResources().getDrawable(R.drawable.rounded_corner));
                sparkAdapter.setPeriod(app().getState().getPortfolioMutableLiveData().getValue().month);
            }
        });

        btnYtd.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                selectedPeriodTextView.setBackgroundResource(android.R.color.transparent);
                selectedPeriodTextView.setTextColor(getResources().getColor(R.color.orange));
                selectedPeriodTextView = btnYtd;
                btnYtd.setTextColor(getResources().getColor(R.color.white));
                view.setBackground(getResources().getDrawable(R.drawable.rounded_corner));
                sparkAdapter.setPeriod(app().getState().getPortfolioMutableLiveData().getValue().ytd);
            }
        });

        btnWeek.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                selectedPeriodTextView.setBackgroundResource(android.R.color.transparent);
                selectedPeriodTextView.setTextColor(getResources().getColor(R.color.orange));
                selectedPeriodTextView = btnWeek;
                btnWeek.setTextColor(getResources().getColor(R.color.white));
                view.setBackground(getResources().getDrawable(R.drawable.rounded_corner));
                sparkAdapter.setPeriod(app().getState().getPortfolioMutableLiveData().getValue().week);
            }
        });

        sparkView.setScrubListener(new SparkView.OnScrubListener() {
            @Override
            public void onScrubbed(Object value) {
                if (value == null) {
                    txtScrubInfo.setText(R.string.scrub_empty);
                } else {
                    txtScrubInfo.setText(getString(R.string.scrub_format, value));
                }
            }
        });

        selectedPeriodTextView = btnDay;
        sparkAdapter.setPeriod(app().getState().getPortfolioMutableLiveData().getValue().day);
        sparkView.setAdapter(sparkAdapter);

        final BaseAdapter listAdapter = new BaseAdapter() {
            public View getView(int position, View convertView, ViewGroup viewGroup) {
                if (convertView == null) convertView = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.convert_main_portfolio_item, viewGroup, false);

                TextView txtTitle = convertView.findViewById(R.id.convert_main_portfolio_item_txt_title);
                TextView txtPercent = convertView.findViewById(R.id.convert_main_portfolio_item_txt_percentage);
                TextView txtPrice = convertView.findViewById(R.id.convert_main_portfolio_item_txt_price);
                TextView txtPricePercent = convertView.findViewById(R.id.convert_main_portfolio_item_txt_price_percent);

                Portfolio.StockItem item = app().getState().getPortfolioMutableLiveData().getValue().stocks.get(position);


                if (item.symbol.equals(selected)) {
                    convertView.setBackgroundColor(getResources().getColor(R.color.yellow));
                    item.percent = item.percent + bidValue;
                }

                txtTitle.setText(item.symbol);
                txtPercent.setText(String.format("%s%%", item.percent));

                txtPrice.setText(String.format("$%s", item.close));
                txtPricePercent.setText(String.format("%.2f", item.jump) + "%");

                txtPrice.setBackgroundResource(item.isPositive ? R.drawable.positive_move : R.drawable.negative_move);
                txtPricePercent.setBackgroundResource(item.isPositive ? R.drawable.positive_move : R.drawable.negative_move);

                txtPricePercent.setVisibility(showPrice ? View.GONE : View.VISIBLE);
                txtPrice.setVisibility(showPrice ? View.VISIBLE : View.GONE);

                convertView.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        showPrice = !showPrice;
                        notifyDataSetChanged();
                    }
                });
                return convertView;
            }

            public int getCount() {
                return app().getState().getPortfolioMutableLiveData().getValue().stocks.size();
            }

            public Object getItem(int i) { return null; }

            public long getItemId(int i) { return 0; }
        };

        listView.setAdapter(listAdapter);
        listView.addHeaderView(vgValue);
        listView.addHeaderView(vgGraph);

        app().getState().getPortfolioMutableLiveData().observe(this, new Observer<Portfolio>() {
            @Override
            public void onChanged(@Nullable Portfolio s) {
                updateValue(s, txtValue);
                sparkAdapter.setPeriod(s.day);
                listAdapter.notifyDataSetChanged();
                if (selected != null) {
                    int position = 2;
                    for (Portfolio.StockItem item : s.stocks) {
                        position++;
                        if (selected.equals(item.symbol)) {
                            listView.setSelection(position);
                            listView.smoothScrollToPosition(position);
                            break;
                        }
                    }
                }
            }
        });

        return rootView;
    }

    private void updateValue(@Nullable Portfolio s, TextView txtValue) {
        if (s.value.close <= 0) return;
        if (s.value.isNegative) {
            txtValue.setTextColor(getResources().getColor(R.color.colorAccent));
            txtValue.setText(s.value.close + " (" + String.format("%.2f", s.value.jump) + "%)");
        } else {
            txtValue.setTextColor(getResources().getColor(R.color.green));
            txtValue.setText(s.value.close + " (+" + String.format("%.2f", s.value.jump) + "%)");
        }
    }

    public static class FineSparkAdapter extends SparkAdapter {
        private float[] yData;
        List<Float> period = new ArrayList<>();

        FineSparkAdapter() {
            yData = new float[period.size()];
        }

        void setPeriod(List<Float> period) {
            yData = new float[period.size()];
            this.period = period;
            init();
        }

        void init() {
            for (int i = 0, count = yData.length; i < count; i++) {
                yData[i] = period.get(i);
            }
            notifyDataSetChanged();
        }

        @Override
        public int getCount() {
            return yData.length;
        }

        @NonNull
        @Override
        public Object getItem(int index) {
            return yData[index];
        }

        @Override
        public float getY(int index) {
            return yData[index];
        }
    }
}