const correctOrder = [
    "Get Approval",
  "Find a Real Estate Agent",
  "Tour Homes",
  "Make an Offer",
  "Finalize a Mortgage",
  "Close the Sale"
];

const createStep = (text) => $(`<div class="step" draggable="true">${text}</div>`);

function makeDraggable($el) {
  $el.draggable({
    helper: function () {
      const $original = $(this);
      const $clone = $original.clone();
      $clone.width($original.width());
      return $clone;
    },
    revert: "invalid",
    appendTo: 'body',
    zIndex: 1000
  });
}

function renderStepBank() {
  $("#steps").empty();
  
  // Shuffle steps before rendering
  const shuffledOrder = [...correctOrder].sort(() => Math.random() - 0.5);

  shuffledOrder.forEach(text => {
    const $step = createStep(text);
    $("#steps").append($step);
    makeDraggable($step);
  });
}


function resetTimeline() {
  $(".timeline-slot").each(function () {
    $(this).removeClass("filled correct incorrect").text("Drop Step");
  });
  $("#resultMessage").text("");
  renderStepBank();
}

function updateCheckButtonState() {
  const filled = $(".timeline-slot").filter(function () {
    return $(this).text().trim() !== "Drop Step";
  }).length;

  const enabled = filled >= 6;

  $("#checkOrderBtn").prop("disabled", !enabled);
  $("#takeQuizBtn").prop("disabled", !enabled);
}

$(function () {
  renderStepBank();

  $(".timeline-slot, #steps").droppable({
    accept: ".step",
    hoverClass: "bg-secondary",
    drop: function (event, ui) {
      const $dropped = ui.draggable.clone().removeClass("ui-draggable-dragging");
      const fromSteps = ui.draggable.parent().attr("id") === "steps";

      const $target = $(this);
      if ($target.hasClass("timeline-slot")) {
        if ($target.children().length > 0) {
          $("#steps").append($target.children().detach());
        }
        $target.empty().append($dropped).addClass("filled");
      } else {
        $("#steps").append($dropped);
      }

      ui.draggable.remove();
      makeDraggable($dropped);
      updateCheckButtonState();
    }
  });

  $("#checkOrderBtn").click(function () {
    const allFilled = $(".timeline-slot").filter(function () {
      return $(this).text().trim() === "Drop Step";
    }).length === 0;

    if (!allFilled) {
      $("#resultMessage").text("⚠️ Please complete all timeline steps before checking.");
      return;
    }

    let allCorrect = true;
    $(".timeline-slot").each(function (i) {
      const actual = $(this).text().trim();
      $(this).removeClass("correct incorrect");
      if (actual === correctOrder[i]) {
        $(this).addClass("correct");
      } else {
        $(this).addClass("incorrect");
        allCorrect = false;
      }
    });

    $("#resultMessage").text(allCorrect ? "✅ Correct Order!" : "❌ Some steps are incorrect. Try again!");
  });

  $("#resetBtn").click(resetTimeline);
});