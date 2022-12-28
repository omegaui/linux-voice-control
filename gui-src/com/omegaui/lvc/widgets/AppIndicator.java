package com.omegaui.lvc.widgets;

import com.omegaui.lvc.App;

import javax.swing.JComponent;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;

public class AppIndicator extends JComponent {

    private final App app;

    public AppIndicator(App app){
        this.app = app;
        setSize(27, 27);
        setPreferredSize(getSize());
    }

    @Override
    public void paint(Graphics graphics) {
        super.paint(graphics);
        Graphics2D g = (Graphics2D)graphics;
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_RENDERING, RenderingHints.VALUE_RENDER_QUALITY);
        g.setColor(app.inferIndicatorColor());
        g.fillRoundRect(0, 0, getWidth(), getHeight(),100, 100);
        g.dispose();
    }
}
