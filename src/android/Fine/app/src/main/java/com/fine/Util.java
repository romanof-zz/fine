package com.fine;

import android.content.Context;
import android.content.res.Resources;
import android.text.Html;
import android.text.method.LinkMovementMethod;
import android.widget.NumberPicker;
import android.widget.TextView;

public class Util {


    public static String formatString(int stringResId, Context context, String... strings) {
        String tmpl = context.getResources().getString(stringResId);
        return strings != null && strings.length > 0 ? String.format(tmpl, strings) : tmpl;
    }

    public static void setText(TextView into, int stringResId, String... strings) {
        Context context = into.getContext();
        String text = formatString(stringResId, context, strings);

        into.setText(text);
        into.setMovementMethod(new LinkMovementMethod());
    }

    public static void setTextHtml(TextView into, int stringResId) {
        setTextHtml(into, stringResId, (String[]) null);
    }

    public static void setTextHtml(TextView into, int stringResId, String... strings) {
        String tmpl = into.getContext().getResources().getString(stringResId);
        String html = strings != null && strings.length > 0 ? String.format(tmpl, strings) : tmpl;

        into.setText(Html.fromHtml(html));
        into.setMovementMethod(LinkMovementMethod.getInstance());
    }

    public static void setDividerColor(NumberPicker picker, Context context) {
        java.lang.reflect.Field[] pickerFields = NumberPicker.class.getDeclaredFields();
        for (java.lang.reflect.Field pf : pickerFields) {
            if (pf.getName().equals("mSelectionDivider")) {
                pf.setAccessible(true);
                try {
                    pf.set(picker, context.getResources().getDrawable(R.color.colorPrimary));
                } catch (IllegalArgumentException | IllegalAccessException | Resources.NotFoundException e) {
                    e.printStackTrace();
                }
                break;
            }
        }
    }
}
