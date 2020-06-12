package com.fine;

import android.content.Context;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextUtils;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.InputMethodManager;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.amulyakhare.textdrawable.TextDrawable;
import com.amulyakhare.textdrawable.util.ColorGenerator;
import com.bumptech.glide.Glide;
import com.fine.data.Comment;
import com.fine.data.Post;
import com.fine.data.User;

public class FragComments extends Fragment {

    public static final String TAG = FragComments.class.getSimpleName();

    private Post post;
    private BaseAdapter adapter;
    private User currentUser;

    public FragComments() {
        currentUser = new User();
        currentUser.name = "Sergii R.";
        currentUser.initials = currentUser.getInitials(currentUser.name);
    }

    public FragComments(Post post) {
        this.post = post;
        //Remove this code after user will be able to login
        currentUser = new User();
        currentUser.name = "Sergii R.";
        currentUser.initials = currentUser.getInitials(currentUser.name);
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull final LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        if (getArguments() != null) {
            this.post = getArguments().getParcelable("post");
            setArguments(null);
        }
        View rootView = inflater.inflate(R.layout.frag_comments, container, false);

        ListView listView = rootView.findViewById(R.id.frag_comments_list);
        final TextView btnSend = rootView.findViewById(R.id.frag_comments_send);
        final TextView commentText = rootView.findViewById(R.id.frag_comments_comment);

        commentText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {}

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {}

            @Override
            public void afterTextChanged(Editable editable) {
                btnSend.setTextColor(TextUtils.isEmpty(commentText.getText()) ? getResources().getColor(R.color.grey) : getResources().getColor(R.color.colorPrimary));
            }
        });

        btnSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (TextUtils.isEmpty(commentText.getText())) return;
                Comment newComment = new Comment();
                newComment.text = commentText.getText().toString();
                newComment.user = currentUser;
                post.comments.add(newComment);
                adapter.notifyDataSetChanged();
                commentText.setText("");
                commentText.clearFocus();
                InputMethodManager imm = (InputMethodManager) getActivity().getSystemService(Context.INPUT_METHOD_SERVICE);
                imm.hideSoftInputFromWindow(commentText.getWindowToken(), 0);
            }
        });

        adapter = new BaseAdapter() {

            public View getView(int pos, View convertView, ViewGroup viewGroup) {

                if (convertView == null) convertView = inflater.inflate(R.layout.convert_comments, viewGroup, false);

                TextView txtComment = convertView.findViewById(R.id.convert_comments_txt);
                ImageView imgUser = convertView.findViewById(R.id.convert_comments_img);
                final TextView txtLikes = convertView.findViewById(R.id.convert_comments_like_txt);
                final ImageView imgLikes = convertView.findViewById(R.id.convert_comments_like_img);
                View likeView = convertView.findViewById(R.id.convert_comments_like_container);
                final Comment comment = post.comments.get(pos);

                txtComment.setText(comment.text);

                if (!TextUtils.isEmpty(comment.user.imageUrl)) {
                    Glide.with(imgUser.getContext())
                            .load(comment.user.imageUrl)
                            .centerCrop()
                            .into(imgUser);
                } else {
                    TextDrawable drawable = TextDrawable.builder()
                            .beginConfig()
                            .width(20)
                            .height(20)
                            .bold()
                            .endConfig()
                            .buildRoundRect(comment.user.initials, ColorGenerator.MATERIAL.getColor(comment.user.initials), 10);

                    imgUser.setImageDrawable(drawable);
                }

                txtLikes.setText(String.format(": %d", comment.likesCount));
                imgLikes.setImageDrawable(getResources().getDrawable(comment.isLiked ? R.drawable.liked : R.drawable.unliked));
                likeView.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        comment.likesCount = comment.isLiked ? comment.likesCount - 1 : comment.likesCount + 1;
                        comment.isLiked = !comment.isLiked;
                        txtLikes.setText(String.format(": %d", comment.likesCount));
                        imgLikes.setImageDrawable(getResources().getDrawable(comment.isLiked ? R.drawable.liked : R.drawable.unliked));

                    }
                });
                return convertView;
            }

            public int getCount() { return post.comments.size(); }

            public Object getItem(int i) { return null; }

            public long getItemId(int i) { return 0; }

        };

        listView.setAdapter(adapter);

        return rootView;
    }


}
