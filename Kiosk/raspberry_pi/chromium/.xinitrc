# disable screensaver
xset s off
# disable screen blanking
xset s noblank
# disable DPMS (Display Power Management Signaling - power-saving feature of your monitor)
xset -dpms

exec chromium  \
--window-position=0,0 \
--start-fullscreen \
--kiosk \
--noerrdialogs \
--disable-translate \
--no-first-run \
--disable-infobars \
--disable-features=TranslateUI \
--disk-cache-dir=/dev/null \
--overscroll-history-navigation=0 \
--disable-pinch \
