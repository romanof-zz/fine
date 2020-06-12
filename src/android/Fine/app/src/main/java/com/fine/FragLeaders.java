package com.fine;

import android.os.Bundle;
import android.text.TextUtils;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;

import com.amulyakhare.textdrawable.TextDrawable;
import com.amulyakhare.textdrawable.util.ColorGenerator;
import com.bumptech.glide.Glide;
import com.fine.data.User;

import java.util.List;

import static com.fine.FineApp.app;

public class FragLeaders extends Fragment {

    private static final String EXPERTS = "EXPERTS";
    private static final String LEADERBOARD = "LEADERBOARD";

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable final ViewGroup container, @Nullable Bundle savedInstanceState) {
        app().downloadLeaders();
        app().downloadExperts();

        View rootView = LayoutInflater.from(container.getContext()).inflate(R.layout.frag_leaders, container, false);
        ListView listView = rootView.findViewById(R.id.frag_leaders_list);

        final BaseAdapter listAdapter = new BaseAdapter() {

            public View getView(int pos, View convertView, ViewGroup viewGroup) {

                if (convertView == null) convertView = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.convert_main_leaders_item, container, false);
                View vgHeader = convertView.findViewById(R.id.convert_main_leaders_header);
                View vgItem = convertView.findViewById(R.id.convert_main_leaders_item);
                TextView txtHeader = vgHeader.findViewById(R.id.convert_main_leaders_header_txt);

                List<User> experts = app().getState().getExpertsMutableLiveData().getValue();
                List<User> leaders = app().getState().getLeadersMutableLiveData().getValue();

                int posExpertsHeader = 0;
                int posLeadersHeader = experts.size() + 1;

                if (pos == posExpertsHeader) {
                    vgItem.setVisibility(View.GONE);
                    vgHeader.setVisibility(View.VISIBLE);
                    txtHeader.setText(EXPERTS);
                } else if (pos == posLeadersHeader) {
                    vgItem.setVisibility(View.GONE);
                    vgHeader.setVisibility(View.VISIBLE);
                    txtHeader.setText(LEADERBOARD);
                } else if (posExpertsHeader < pos && pos < posLeadersHeader) {
                    vgItem.setVisibility(View.VISIBLE);
                    vgHeader.setVisibility(View.GONE);
                    // expert
                    User expert = experts.get(pos - posExpertsHeader - 1);
                    setupUserConvert(vgItem, expert);
                } else   /* posLeadersHeader < pos */ {
                    vgItem.setVisibility(View.VISIBLE);
                    vgHeader.setVisibility(View.GONE);
                    // leader
                    User leader = leaders.get(pos - posLeadersHeader - 1);
                    setupUserConvert(vgItem, leader);
                }

                return convertView;
            }

            public int getCount() {
                return app().getState().getExpertsMutableLiveData().getValue().size()
                        + app().getState().getLeadersMutableLiveData().getValue().size()
                        + 2;
            }

            public Object getItem(int pos) { return null; }

            public long getItemId(int i) { return 0; }

        };
        listView.setAdapter(listAdapter);

        Observer<List<User>> onChangeObserver = new Observer<List<User>>() {
            public void onChanged(@Nullable List<User> s) {
                listAdapter.notifyDataSetChanged();
            }
        };
        app().getState().getExpertsMutableLiveData().observe(this, onChangeObserver);
        app().getState().getLeadersMutableLiveData().observe(this, onChangeObserver);

        return rootView;
    }

    private static void setupUserConvert(final View convertView, final User user) {
        ImageView imageView = convertView.findViewById(R.id.convert_main_leaders_item_img);
        TextView valueView = convertView.findViewById(R.id.convert_main_leaders_value);
        final TextView followView = convertView.findViewById(R.id.convert_main_leaders_follow);
        TextView titleView = convertView.findViewById(R.id.convert_main_leaders_item_txt_title);
        TextView subTitleView = convertView.findViewById(R.id.convert_main_leaders_item_txt_subtitle);

        followView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                user.isFollowed = !user.isFollowed;
                followView.setText(user.isFollowed ? R.string.followed : R.string.follow);
                followView.setBackgroundColor(convertView.getContext().getResources().getColor(user.isFollowed ? R.color.grey : R.color.colorPrimary));
            }
        });

        if (!TextUtils.isEmpty(user.imageUrl)) {
            Glide.with(convertView.getContext())
                    .load(user.imageUrl)
                    .centerCrop()
                    .into(imageView);
        } else {
            TextDrawable drawable = TextDrawable.builder()
                    .beginConfig()
                    .width(20)
                    .height(20)
                    .bold()
                    .endConfig()
                    .buildRoundRect(user.initials, ColorGenerator.MATERIAL.getColor(user.initials), 10);

            imageView.setImageDrawable(drawable);
        }

        valueView.setText(String.format("%d", user.value));
        titleView.setText(user.name);
        subTitleView.setText(user.description);
        subTitleView.setVisibility(TextUtils.isEmpty(user.description) ? View.GONE : View.VISIBLE);

        followView.setText(user.isFollowed ? R.string.followed : R.string.follow);
        followView.setBackgroundColor(convertView.getContext().getResources().getColor(user.isFollowed ? R.color.grey : R.color.colorPrimary));
    }
}
