package com.omegaui.lvc.widgets;

import com.omegaui.lvc.App;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

import static com.omegaui.lvc.AppConstants.textColor;
import static com.omegaui.lvc.AppConstants.textFont;

public class CloseButton extends JComponent {

    private volatile boolean hover = false;

    public CloseButton(final App app){
        setSize(50, 20);
        setPreferredSize(getSize());
        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseEntered(MouseEvent e) {
                hover = true;
                repaint();
            }

            @Override
            public void mouseExited(MouseEvent e) {
                hover = false;
                repaint();
            }

            @Override
            public void mouseClicked(MouseEvent e) {
                new Thread(() -> {
                    app.setStatus("quitting program");
                    try {
                        Thread.sleep(2000);
                    } catch (InterruptedException ex) {
                        throw new RuntimeException(ex);
                    }
                    System.exit(0);
                }).start();
            }
        });
    }

    @Override
    public void paint(Graphics graphics) {
        Graphics2D g = (Graphics2D)graphics;
        g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_RENDERING, RenderingHints.VALUE_RENDER_QUALITY);
        g.setColor(Color.WHITE);
        g.fillRoundRect(0, 0, getWidth(), getHeight(), 10, 10);
        g.setColor(hover ? Color.BLACK : Color.gray);
        g.setFont(textFont);
        g.drawString("quit", getWidth()/2 - g.getFontMetrics().stringWidth("quit")/2, getHeight()/2 - g.getFontMetrics().getHeight()/2 + g.getFontMetrics().getAscent() - g.getFontMetrics().getDescent() + 1);
    }
}
