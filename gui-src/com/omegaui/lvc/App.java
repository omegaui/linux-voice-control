package com.omegaui.lvc;

import com.omegaui.lvc.widgets.AppIndicator;
import com.omegaui.lvc.widgets.CloseButton;

import javax.swing.JPanel;
import javax.swing.JWindow;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;
import java.awt.geom.RoundRectangle2D;

import static com.omegaui.lvc.AppConstants.*;

public class App extends JWindow {

    private int mousePressX;
    private int mousePressY;

    private volatile int tag = -1;
    private volatile String status = "linux-voice-control";

    private App(){
        initListeners();
        pack();
        setSize(180, 100);
        setLocationRelativeTo(null);
        setAlwaysOnTop(true);
        initUI();
        setVisible(true);
    }

    private void initListeners(){
        addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                mousePressX = e.getX();
                mousePressY = e.getY();
            }
        });

        addMouseMotionListener(new MouseMotionAdapter() {
            @Override
            public void mouseDragged(MouseEvent e) {
                setLocation(e.getXOnScreen() - mousePressX, e.getYOnScreen() - mousePressY);
            }
        });
    }

    private void initUI(){
        JPanel panel = new JPanel(null);
        panel.setBackground(transparency);
        setShape(new RoundRectangle2D.Double(0, 0, getWidth(),getHeight(),20,20));
        setBackground(transparency);
        setContentPane(panel);

        AppIndicator indicator = new AppIndicator(this);
        indicator.setLocation(getWidth()/2 - indicator.getWidth()/2, 20);
        add(indicator);

        CloseButton closeButton = new CloseButton(this);
        closeButton.setLocation(getWidth() - 70, 10);
        add(closeButton);
    }

    @Override
    public void paint(Graphics gx) {
        Graphics2D g = (Graphics2D)gx;
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_RENDERING, RenderingHints.VALUE_RENDER_SPEED);
        super.paint(g);
        g.setColor(backgroundColor);
        g.fillRect(0, 0, getWidth(), getHeight());
        g.setColor(textColor);
        g.setFont(textFont);
        g.drawString(inferIndicatorText(), getWidth()/2 - g.getFontMetrics().stringWidth(inferIndicatorText())/2, (getHeight() - 50) + g.getFontMetrics().getAscent() - g.getFontMetrics().getDescent() + 3);
        g.setFont(textFont.deriveFont(Font.PLAIN));
        g.drawString(status, getWidth()/2 - g.getFontMetrics().stringWidth(status)/2, (getHeight() - 30) + g.getFontMetrics().getAscent() - g.getFontMetrics().getDescent() + 3);
        g.dispose();
    }

    public Color inferIndicatorColor(){
        return switch (tag){
            case STARTED_TAG -> startedColor;
            case LISTENING_TAG -> listeningColor;
            case ERROR_TAG -> errorColor;
            case EXECUTING_TAG -> executingColor;
            case COMPUTING_TAG -> computingColor;
            default -> startingColor;
        };
    }

    public String inferIndicatorText(){
        return switch (tag){
            case STARTED_TAG -> "started...";
            case LISTENING_TAG -> "listening...";
            case ERROR_TAG -> "error...";
            case EXECUTING_TAG -> "executing...";
            case COMPUTING_TAG -> "computing...";
            default -> "starting...";
        };
    }

    public static void main(String[] args) {
        App app = new App();
        LVCHandler lvcHandler = new LVCHandler(app);
        lvcHandler.launch();
    }

    public void setTag(int tag) {
        this.tag = tag;
        repaint();
    }

    public void setStatus(String status) {
        this.status = status;
        repaint();
    }
}
