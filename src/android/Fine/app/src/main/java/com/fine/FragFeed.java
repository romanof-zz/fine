package com.fine;

import android.app.AlertDialog;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.NumberPicker;
import android.widget.TextView;

import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.navigation.NavController;
import androidx.navigation.fragment.NavHostFragment;

import com.amulyakhare.textdrawable.TextDrawable;
import com.amulyakhare.textdrawable.util.ColorGenerator;
import com.bumptech.glide.Glide;
import com.fine.data.Post;

import java.util.ArrayList;
import java.util.List;

import static com.fine.FineApp.app;

public class FragFeed extends Fragment {

    private static final String VIDEO = "video";
    private static final String BID_MADE = "BID MADE";
    private BaseAdapter adapter;
    private String[] pickerValues;

    public FragFeed() {
        initPickerValues();
    }

    public View onCreateView(LayoutInflater inflater, final ViewGroup container, Bundle savedInstanceState) {
        app().downloadPosts();

        app().getState().getFeed().observe(this, new Observer<List<Post>>() {
            public void onChanged(List<Post> posts) {
                adapter.notifyDataSetChanged();
            }
        });

        View root           = inflater.inflate(R.layout.frag_feed, container, false);
        ListView listFeed   = root.findViewById(R.id.frag_feed_list);
        final NavController navController = NavHostFragment.findNavController(this);

        adapter = new BaseAdapter() {
            public View getView(int position, View convertView, ViewGroup viewGroup) {
                if (convertView == null)
                    convertView = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.convert_main_feed_item, viewGroup, false);

                View postView           = convertView.findViewById(R.id.convert_main_feed_post_item);
                View videoView          = convertView.findViewById(R.id.convert_main_feed_video_item);
                View likeViewGroup      = convertView.findViewById(R.id.convert_main_feed_item_like_layout);
                TextView txtTitle       = convertView.findViewById(R.id.convert_main_feed_item_txt_title);
                ImageView imageView     = convertView.findViewById(R.id.convert_main_feed_item_img);
                final ImageView likeView = convertView.findViewById(R.id.like);
                final ImageView biddedView = convertView.findViewById(R.id.bidded_imageView);
                final TextView txtLikes = convertView.findViewById(R.id.convert_main_feed_item_txt_likes);
                TextView txtComments    = convertView.findViewById(R.id.convert_main_feed_item_txt_comments);
                View vgComments         = convertView.findViewById(R.id.convert_main_feed_item_comments_container);
                final TextView txtBid   = convertView.findViewById(R.id.convert_main_feed_item_txt_type);
                ImageView videoImage    = convertView.findViewById(R.id.convert_main_feed_video_item_img);
                ImageView btnPlay       = convertView.findViewById(R.id.convert_main_feed_video_item_playbutton);

                final Post item = app().getState().getFeed().getValue().get(position);
                if (VIDEO.equals(item.type)) {
                    postView.setVisibility(View.GONE);
                    videoView.setVisibility(View.VISIBLE);

                    btnPlay.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View view) {
                            Bundle bundle = new Bundle();
                            bundle.putString("url", item.details.url);
                            navController.navigate(R.id.action_nav_main_to_nav_youtube, bundle);
                        }
                    });

                    Glide.with(convertView.getContext())
                            .load(item.details.previewImageUrl)
                            .into(videoImage);
                } else {
                    postView.setVisibility(View.VISIBLE);
                    videoView.setVisibility(View.GONE);
                    View bidView = convertView.findViewById(R.id.convert_main_feed_item_bid);
                    bidView.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View view) {
                            if (txtBid.getText().equals(BID_MADE)) return;
                            final View customLayout = getLayoutInflater().inflate(R.layout.bid_dialog_layout, null);
                            final NumberPicker picker = customLayout.findViewById(R.id.bid_dialog_numberPicker);
                            Button cancelButton = customLayout.findViewById(R.id.bid_dialog_cancel);
                            final Button bidButton = customLayout.findViewById(R.id.bid_dialog_bid);
                            TextView txtBidTitle = customLayout.findViewById(R.id.bid_dialog_title);
                            txtBidTitle.setText(String.format("%s at $%s", item.details.symbol, item.details.price));

                            Util.setDividerColor(picker, view.getContext());
                            picker.setMinValue(0);
                            picker.setMaxValue(999);
                            picker.setValue(9);
                            picker.setDisplayedValues(pickerValues);

                            final AlertDialog dialog = new AlertDialog.Builder(getContext())
                                    .setView(customLayout)
                                    .create();

                            bidButton.setOnClickListener(new View.OnClickListener() {
                                @Override
                                public void onClick(View view) {
                                    String[] val = pickerValues[picker.getValue()].split("%");
                                    Bundle bundle = new Bundle();
                                    bundle.putString(FragPortfolio.SELECTED_SYMBOL, item.details.symbol);
                                    bundle.putDouble(FragPortfolio.BID_VALUE, Double.parseDouble(val[0]));

                                    dialog.dismiss();

                                    txtBid.setText(BID_MADE);
                                    biddedView.setVisibility(View.VISIBLE);

                                    navController.navigate(R.id.navigation_portfolio, bundle);
                                }
                            });

                            cancelButton.setOnClickListener(new View.OnClickListener() {
                                @Override
                                public void onClick(View view) {
                                    dialog.dismiss();
                                }
                            });
                            dialog.show();
                        }
                    });

                    TextDrawable drawable = TextDrawable.builder()
                            .beginConfig()
                            .width(20)
                            .height(20)
                            .bold()
                            .endConfig()
                            .buildRoundRect(item.user.initials, ColorGenerator.MATERIAL.getColor(item.user.initials), 10);
                    imageView.setImageDrawable(drawable);

                    Util.setTextHtml(txtTitle, "buy".equals(item.details.action)
                                    ? R.string.convert_feed_item_title_bought_3p
                                    : R.string.convert_feed_item_title_sold_3p,
                            item.user.name, item.details.symbol, "$" + item.details.price
                    );

                    txtLikes.setText(String.format(": %d", item.likesCount));
                    likeView.setImageDrawable(item.isLiked ? getResources().getDrawable(R.drawable.liked) : getResources().getDrawable(R.drawable.unliked));

                    txtComments.setText(String.format("%d", item.commentsCount));
                    vgComments.setOnClickListener(new View.OnClickListener() {
                        public void onClick(View view) {
                            Bundle bundle = new Bundle();
                            bundle.putParcelable("post", item);
                            navController.navigate(R.id.action_nav_main_to_nav_comments, bundle);
                        }
                    });

                    txtBid.setText(item.isBidded ? BID_MADE : "BID");
                    biddedView.setVisibility(item.isBidded ? View.VISIBLE : View.INVISIBLE);

                    likeViewGroup.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View view) {
                            item.isLiked = !item.isLiked;
                            item.likesCount = item.isLiked ? item.likesCount + 1 : item.likesCount - 1;
                            txtLikes.setText(String.format(": %d", item.likesCount));
                            likeView.setImageDrawable(getResources().getDrawable(item.isLiked ? R.drawable.liked : R.drawable.unliked));
                        }
                    });
                }

                return convertView;
            }

            public int getCount() {
                return app().getState().getFeed().getValue().size();
            }

            public long getItemId(int i) { return 0;    }
            public Object getItem(int i) { return null; }

        };
        listFeed.setAdapter(adapter);
        return root;
    }

    private void initPickerValues() {
        List<String> list = new ArrayList<>();
        for (double i = 0.1; i < 100; i += 0.1) {
            list.add("" + String.format("%.1f", i) + "%");
        }
        pickerValues = new String[list.size()];
        pickerValues = list.toArray(pickerValues);
    }

}