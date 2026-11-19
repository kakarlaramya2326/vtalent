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

(() => {
  const dialog = document.querySelector(".registration-modal");
  const form = document.querySelector(".registration-modal form");
  const closeLink = dialog?.querySelector(".registration-modal-close");
  if (!dialog || !form || !closeLink) {
    return;
  }

  dialog.focus({ preventScroll: true });

  dialog.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      window.location.assign(closeLink.href);
      return;
    }

    if (event.key !== "Tab") {
      return;
    }

    const focusableElements = dialog.querySelectorAll(
      'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"])',
    );
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    if (
      event.shiftKey &&
      (document.activeElement === dialog ||
        document.activeElement === firstElement)
    ) {
      event.preventDefault();
      lastElement.focus();
    } else if (!event.shiftKey && document.activeElement === lastElement) {
      event.preventDefault();
      firstElement.focus();
    }
  });

  const courseInput = form.querySelector("#selected-course");
  const courseButtons = Array.from(
    document.querySelectorAll(".registration-course-choice"),
  );
  const courseGroups = Array.from(
    document.querySelectorAll(".registration-course-set"),
  );
  const courseStatus = form.querySelector(".registration-course-status");
  const submitLabel = form.querySelector(".registration-submit-label");
  const programInputs = Array.from(
    form.querySelectorAll('input[name="program_type"]'),
  );

  const getProgramType = () => {
    const selectedProgram = programInputs.find((input) => input.checked);
    return selectedProgram ? selectedProgram.value : "coaching";
  };

  const updateCourseGroups = () => {
    const activeProgramType = getProgramType();
    courseGroups.forEach((group) => {
      group.hidden = group.dataset.programType !== activeProgramType;
    });
  };

  const updateSubmitLabel = () => {
    const selectedCourse = courseButtons.find(
      (button) => button.dataset.courseSlug === courseInput.value,
    );

    if (selectedCourse) {
      submitLabel.textContent = `Continue with ${selectedCourse.dataset.courseLabel}`;
    } else if (getProgramType() === "internship") {
      submitLabel.textContent = "Explore internships";
    } else {
      submitLabel.textContent = "Continue to courses";
    }
  };

  const selectCourse = (slug) => {
    courseInput.value = slug;
    const selectedCourse = courseButtons.find(
      (button) => button.dataset.courseSlug === slug,
    );

    courseButtons.forEach((button) => {
      const isSelected = button.dataset.courseSlug === slug;
      button.classList.toggle("is-selected", isSelected);
      button.setAttribute("aria-pressed", String(isSelected));
    });

    if (selectedCourse) {
      const programLabel =
        selectedCourse.dataset.programType === "internship"
          ? "internship"
          : "course";
      courseStatus.textContent = `Selected: ${selectedCourse.dataset.courseLabel} · ${selectedCourse.dataset.courseDuration} ${programLabel}`;
    } else {
      courseStatus.textContent =
        getProgramType() === "internship"
          ? "Choose a 45-day internship card above."
          : "Choose a course card or select a 45-day internship.";
    }

    updateCourseGroups();
    updateSubmitLabel();
  };

  courseButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const programOption = programInputs.find(
        (input) => input.value === button.dataset.programType,
      );
      if (programOption && !programOption.checked) {
        programOption.checked = true;
        programOption.dispatchEvent(new Event("change", { bubbles: true }));
      }
      selectCourse(button.dataset.courseSlug);
    });
  });

  programInputs.forEach((input) => {
    input.addEventListener("change", () => {
      if (input.checked) {
        selectCourse("");
      }
    });
  });

  updateCourseGroups();
  updateSubmitLabel();
})();
