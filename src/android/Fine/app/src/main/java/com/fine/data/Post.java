package com.fine.data;

import android.net.Uri;
import android.os.Parcel;
import android.os.Parcelable;
import android.text.TextUtils;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class Post implements Parcelable {

    public int id;

    public String type;
    public String timestamp;
    public User user;
    public PostDetails details;
    public boolean isLiked;
    public int likesCount;
    public int commentsCount;
    public boolean isBidded;
    public List<Comment> comments = new ArrayList<>();

    public Post() {}

    protected Post(Parcel in) {
        id = in.readInt();
        type = in.readString();
        timestamp = in.readString();
        user = in.readParcelable(User.class.getClassLoader());
        details = in.readParcelable(PostDetails.class.getClassLoader());
        isLiked = in.readByte() != 0;
        likesCount = in.readInt();
        commentsCount = in.readInt();
        isBidded = in.readByte() != 0;
        comments = in.createTypedArrayList(Comment.CREATOR);
    }

    public static final Creator<Post> CREATOR = new Creator<Post>() {
        @Override
        public Post createFromParcel(Parcel in) {
            return new Post(in);
        }

        @Override
        public Post[] newArray(int size) {
            return new Post[size];
        }
    };

    public Post parse(JSONObject json) {
        this.id = json.optInt("id");
        this.type = json.optString("type");
        this.timestamp = json.optString("timestamp");
        User user = new User();
        this.user = user.parse(json.optJSONObject("user"));
        PostDetails details = new PostDetails();
        this.details = details.parse(json.optJSONObject("details"));
        this.isBidded = json.optBoolean("is_bidded");
        this.isLiked = json.optBoolean("is_liked");
        this.likesCount = json.optInt("like_cnt");
        this.commentsCount = json.optInt("comment_cnt");
        JSONArray commentsJson = json.optJSONArray("comments");
        if (commentsJson != null) {
            List<Comment> comments = new ArrayList<>();
            for (int i = 0; i < commentsJson.length(); i++) {
                Comment comment = new Comment();
                comments.add(comment.parse(commentsJson.optJSONObject(i)));
            }
            this.comments = comments;

        }
        return this;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel parcel, int i) {
        parcel.writeInt(id);
        parcel.writeString(type);
        parcel.writeString(timestamp);
        parcel.writeParcelable(user, i);
        parcel.writeParcelable(details, i);
        parcel.writeByte((byte) (isLiked ? 1 : 0));
        parcel.writeInt(likesCount);
        parcel.writeInt(commentsCount);
        parcel.writeByte((byte) (isBidded ? 1 : 0));
        parcel.writeTypedList(comments);
    }


    public static class PostDetails implements Parcelable {
        public String symbol;
        public double price;
        public String action;
        public String url;
        public String videoId;
        public String previewImageUrl;

        public PostDetails(){}

        protected PostDetails(Parcel in) {
            symbol = in.readString();
            price = in.readDouble();
            action = in.readString();
            url = in.readString();
            videoId = in.readString();
            previewImageUrl = in.readString();
        }

        public static final Creator<PostDetails> CREATOR = new Creator<PostDetails>() {
            @Override
            public PostDetails createFromParcel(Parcel in) {
                return new PostDetails(in);
            }

            @Override
            public PostDetails[] newArray(int size) {
                return new PostDetails[size];
            }
        };

        public PostDetails parse(JSONObject json) {
            this.symbol = json.optString("symbol");
            this.price = json.optDouble("price");
            this.action = json.optString("action");
            this.url = json.optString("url");
            this.videoId = parseVideoId(this.url);
            this.previewImageUrl = parsePreviewImageUrl(this.videoId);
            return this;
        }

        private String parseVideoId(String url) {
            if (TextUtils.isEmpty(url)) return "";
            Uri uri = Uri.parse(url);
            return uri.getQueryParameter("v");
        }

        private String parsePreviewImageUrl(String videoId) {
            if (TextUtils.isEmpty(videoId)) return "";
            return "https://img.youtube.com/vi/" + videoId + "/0.jpg";
        }

        @Override
        public int describeContents() {
            return 0;
        }

        @Override
        public void writeToParcel(Parcel parcel, int i) {
            parcel.writeString(symbol);
            parcel.writeDouble(price);
            parcel.writeString(action);
            parcel.writeString(url);
            parcel.writeString(videoId);
            parcel.writeString(previewImageUrl);
        }
    }
}
