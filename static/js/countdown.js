(function () {
    "use strict";

    class CountdownTimer {
        constructor(elementId, endTimeIso) {
            this.element = document.getElementById(elementId);
            if (!this.element) {
                return;
            }
            this.endTime = new Date(endTimeIso).getTime();
            this.expiredMessage =
                this.element.dataset.expiredMessage || "Offer Expired";
            this.container = this.element;

            this.init();
        }

        init() {
            this.update();
            this.interval = setInterval(() => this.update(), 1000);
        }

        update() {
            const now = new Date().getTime();
            const distance = this.endTime - now;

            if (distance < 0) {
                this.handleExpired();
                return;
            }

            const time = this.calculateTime(distance);
            this.render(time);
        }

        calculateTime(distance) {
            return {
                days: Math.floor(distance / (1000 * 60 * 60 * 24)),
                hours: Math.floor(
                    (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
                ),
                minutes: Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)),
                seconds: Math.floor((distance % (1000 * 60)) / 1000),
            };
        }

        render(time) {
            let html = '<div class="countdown-timer">';

            if (time.days > 0) {
                html += this.renderUnit(time.days, "Days");
            }

            html += this.renderUnit(time.hours, "Hours");
            html += this.renderUnit(time.minutes, "Mins");
            html += this.renderUnit(time.seconds, "Secs");

            html += "</div>";
            this.container.innerHTML = html;
        }

        renderUnit(value, label) {
            const paddedValue = String(value).padStart(2, "0");
            return `
                <div class="countdown-unit">
                    <div class="countdown-value">${paddedValue}</div>
                    <div class="countdown-label">${label}</div>
                </div>
            `;
        }

        handleExpired() {
            clearInterval(this.interval);
            this.container.innerHTML = `
                <div class="countdown-expired">
                    ${this.expiredMessage}
                </div>
            `;
            const expiredEvent = new CustomEvent("countdown-expired", {
                detail: { elementId: this.element.id },
            });
            document.dispatchEvent(expiredEvent);
        }
    }

    window.CountdownTimer = CountdownTimer;

    document.addEventListener("DOMContentLoaded", function () {
        const countdownElements = document.querySelectorAll("[data-countdown]");

        countdownElements.forEach(function (element) {
            const endTime = element.dataset.countdown;
            const id = element.id || "countdown-" + Math.random().toString(36).substr(2, 9);
            element.id = id;
            new CountdownTimer(id, endTime);
        });
    });
})();
