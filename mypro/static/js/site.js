(() => {
  const progress = document.querySelector(".reading-progress");
  const progressBar = document.querySelector(".reading-progress-bar");
  const backToTop = document.querySelector(".back-to-top");
  const navigation = document.querySelector("#mainNavigation");

  if (!progress || !progressBar || !backToTop) {
    return;
  }

  let updatePending = false;

  const updateScrollControls = () => {
    const scrollableHeight =
      document.documentElement.scrollHeight - window.innerHeight;
    const scrollTop = Math.max(
      window.scrollY || document.documentElement.scrollTop,
      0,
    );
    const percentage =
      scrollableHeight > 0
        ? Math.min((scrollTop / scrollableHeight) * 100, 100)
        : 0;

    progressBar.style.transform = `scaleX(${percentage / 100})`;
    progress.setAttribute("aria-valuenow", String(Math.round(percentage)));
    backToTop.hidden = scrollTop < 400;
    updatePending = false;
  };

  const requestScrollUpdate = () => {
    if (!updatePending) {
      updatePending = true;
      window.requestAnimationFrame(updateScrollControls);
    }
  };

  window.addEventListener("scroll", requestScrollUpdate, { passive: true });
  window.addEventListener("resize", requestScrollUpdate);
  backToTop.addEventListener("click", () => {
    const reduceMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
    window.scrollTo({
      top: 0,
      behavior: reduceMotion ? "auto" : "smooth",
    });
  });

  navigation?.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", () => {
      if (
        navigation.classList.contains("show") &&
        window.bootstrap?.Collapse
      ) {
        window.bootstrap.Collapse.getOrCreateInstance(navigation).hide();
      }
    });
  });

  updateScrollControls();
})();
