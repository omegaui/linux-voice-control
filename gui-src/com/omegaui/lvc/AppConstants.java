package com.omegaui.lvc;

import java.awt.Color;
import java.awt.Font;

public class AppConstants {

    protected static final Color transparency = new Color(240, 240, 240, 0);
    protected static final Color backgroundColor = new Color(170, 170, 170, 20);
    protected static final Color listeningColor = Color.decode("#12E165");
    protected static final Color computingColor = new Color(255, 255, 100);
    protected static final Color executingColor = new Color(100, 200, 255);
    protected static final Color errorColor = new Color(255, 100, 100);
    protected static final Color startingColor = new Color(100, 100, 200);
    protected static final Color startedColor = new Color(200, 100, 20);
    public static final Color textColor = Color.WHITE;
    public static final Font textFont = new Font("Ubuntu Mono", Font.BOLD, 14);

    protected static final int STARTED_TAG = 10;
    protected static final int LISTENING_TAG = 0;
    protected static final int COMPUTING_TAG = 1;
    protected static final int EXECUTING_TAG = 2;
    protected static final int ERROR_TAG = 3;
}
