package com.fine.data;

import android.os.Parcel;
import android.os.Parcelable;
import android.text.TextUtils;

import org.json.JSONObject;

public class User implements Parcelable {
    public int id;
    public String name;
    public String type;
    public String initials;
    public String description;
    public boolean isFollowed;
    public String imageUrl;
    public int value;

    public User() {}

    protected User(Parcel in) {
        id = in.readInt();
        name = in.readString();
        type = in.readString();
        initials = in.readString();
        description = in.readString();
        isFollowed = in.readByte() != 0;
        imageUrl = in.readString();
        value = in.readInt();
    }

    public static final Creator<User> CREATOR = new Creator<User>() {
        @Override
        public User createFromParcel(Parcel in) {
            return new User(in);
        }

        @Override
        public User[] newArray(int size) {
            return new User[size];
        }
    };

    public User parse(JSONObject json) {
        this.id = json.optInt("user_id");
        this.type = json.optString("type");
        this.name = json.optString("name");
        this.initials = getInitials(this.name);
        this.imageUrl = json.optString("image_url");
        this.description = json.optString("desc");
        this.isFollowed = json.optBoolean("is_followed");
        this.value = json.optInt("value");
        return this;
    }

    public String getInitials(String name) {
        if (TextUtils.isEmpty(name)) return "??";
        String[] names = name.split(" ");
        if (names.length > 1) {
            return names[0].substring(0, 1) + names[1].substring(0, 1);
        } else {
            return name.substring(0, 2);
        }
    }


    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel parcel, int i) {
        parcel.writeInt(id);
        parcel.writeString(name);
        parcel.writeString(type);
        parcel.writeString(initials);
        parcel.writeString(description);
        parcel.writeByte((byte) (isFollowed ? 1 : 0));
        parcel.writeString(imageUrl);
        parcel.writeInt(value);
    }
}
