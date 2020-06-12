package com.fine;

import androidx.lifecycle.MutableLiveData;

import com.fine.data.Portfolio;
import com.fine.data.Post;
import com.fine.data.User;

import org.jetbrains.annotations.NotNull;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class FineApp {
    private static final String TAG = FineApp.class.getSimpleName();
    private static final boolean debug = BuildConfig.DEBUG;

    private static FineApp instance;
    private final Application application;

    private static OkHttpClient client = new OkHttpClient();

    public static FineApp app() {
        if (instance == null) throw new IllegalStateException("Application is not created yet!");
        return instance;
    }

    private State state;
    public State        getState() { return state; }
    public Application  application() { return application;}

    public FineApp(Application application) {
        if (instance != null) throw new IllegalStateException("App is recreated! Before:\n" + instance + "\nnow:\n" + this);
        this.application = application;
        instance = this;
    }

    public static class State {
        private MutableLiveData<List<Post>> feed = new MutableLiveData<>();
        private MutableLiveData<List<User>> leadersMutableLiveData = new MutableLiveData<>();
        private MutableLiveData<List<User>> expertsMutableLiveData = new MutableLiveData<>();
        private MutableLiveData<Portfolio> portfolioMutableLiveData = new MutableLiveData<>();

        private State() {
            feed.setValue(new ArrayList<Post>());
            leadersMutableLiveData.setValue(new ArrayList<User>());
            expertsMutableLiveData.setValue(new ArrayList<User>());
            portfolioMutableLiveData.setValue(new Portfolio());
        }

        public MutableLiveData<List<Post>> getFeed() {
            return feed;
        }
        public MutableLiveData<List<User>> getExpertsMutableLiveData() {
            return expertsMutableLiveData;
        }
        public MutableLiveData<List<User>> getLeadersMutableLiveData() {
            return leadersMutableLiveData;
        }
        public MutableLiveData<Portfolio> getPortfolioMutableLiveData() {
            return portfolioMutableLiveData;
        }

    }

    private void onCreate() {
        this.state = new State();
    }

    //
    // Network
    //
    public void downloadPosts() {
        Request request = new Request.Builder()
                .url("https://finedata.org/posts")
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                ArrayList<Post> posts = new ArrayList<>();
                try {
                    JSONArray allJSONArray = new JSONArray(response.body().string());

                    for (int i = 0; i < allJSONArray.length(); i++) {
                        Post post = new Post();
                        post.parse(allJSONArray.getJSONObject(i));
                        posts.add(post);
                    }
                    state.feed.postValue(posts);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    public void downloadExperts() {
        Request request = new Request.Builder()
                .url("https://finedata.org/experts")
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                try {
                    ArrayList<User> experts = new ArrayList<>();
                    JSONArray expertsJson = new JSONArray(response.body().string());

                    for (int i = 0; i < expertsJson.length(); i++) {
                        User user = new User();
                        user.parse(expertsJson.getJSONObject(i));
                        experts.add(user);
                    }
                    state.expertsMutableLiveData.postValue(experts);
                } catch (JSONException e) {
                    e.printStackTrace();
                }

            }
        });

    }

    public void downloadLeaders() {
        Request request = new Request.Builder()
                .url("https://finedata.org/users")
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                try {
                    ArrayList<User> leaders = new ArrayList<>();
                    JSONArray leadersJson = new JSONArray(response.body().string());

                    for (int i = 0; i < leadersJson.length(); i++) {
                        User user = new User();
                        user.parse(leadersJson.getJSONObject(i));
                        leaders.add(user);
                    }

                    state.leadersMutableLiveData.postValue(leaders);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    public void downloadPortfolio() {
        Request request = new Request.Builder()
                .url("https://finedata.org/portfolio")
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                try {
                    Portfolio portfolio = new Portfolio();
                    JSONObject portfolioJson = new JSONObject(response.body().string());
                    portfolio.fromJSON(portfolioJson);
                    state.portfolioMutableLiveData.postValue(portfolio);
                } catch (JSONException e) {
                    e.printStackTrace();
                }

            }
        });

    }

    public static void follow(int userId) {
        String json = "{\"user_id\":" + userId + "}";

        RequestBody body = RequestBody.create(
                MediaType.parse("application/json"), json);

        Request request = new Request.Builder()
                .url("https://finedata.org/follow")
                .post(body)
                .build();

        Call call = client.newCall(request);
        call.enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {

            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {

            }
        });
    }

    public static class Application extends android.app.Application {
        private final FineApp app;

        public Application() { this.app = new FineApp(this); }

        public void onCreate() {
            super.onCreate();
            app.onCreate();
        }
    }
}
