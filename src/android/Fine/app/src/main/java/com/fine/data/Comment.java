package com.fine.data;

import android.os.Parcel;
import android.os.Parcelable;

import org.json.JSONObject;

public class Comment implements Parcelable {
    public int id;
    public String text;
    public User user;
    public double timestamp;
    public boolean isLiked;
    public int likesCount;

    public Comment(){}

    protected Comment(Parcel in) {
        id = in.readInt();
        text = in.readString();
        user = in.readParcelable(User.class.getClassLoader());
        timestamp = in.readDouble();
        isLiked = in.readByte() != 0;
        likesCount = in.readInt();
    }

    public static final Creator<Comment> CREATOR = new Creator<Comment>() {
        @Override
        public Comment createFromParcel(Parcel in) {
            return new Comment(in);
        }

        @Override
        public Comment[] newArray(int size) {
            return new Comment[size];
        }
    };

    public Comment parse(JSONObject json) {
        this.id = json.optInt("id");
        User user = new User();
        this.user = user.parse(json.optJSONObject("user"));
        this.text = json.optString("text");
        this.timestamp = json.optDouble("timestamp");
        this.isLiked = json.optBoolean("is_liked");
        this.likesCount = json.optInt("like_cnt");
        return this;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel parcel, int i) {
        parcel.writeInt(id);
        parcel.writeString(text);
        parcel.writeParcelable(user, i);
        parcel.writeDouble(timestamp);
        parcel.writeByte((byte) (isLiked ? 1 : 0));
        parcel.writeInt(likesCount);
    }
}
