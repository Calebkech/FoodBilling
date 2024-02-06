// transaction_form.js
$(document).ready(function() {
    // Get the jQuery objects for the category and account fields.
    var categoryField = $('#id_category'); // Replace 'id_category' with the actual ID of the category field.
    var accountField = $('#id_account');   // Replace 'id_account' with the actual ID of the account field.
    var accountLabel = $('#id_account_label'); // Target the label associated with the 'account' field.
  
    // Initially hide the account field and its label.
    accountField.hide();
    accountLabel.hide();
  
    // Listen for changes to the category field.
    categoryField.change(function() {
      // Get the value of the category field.
      var categoryValue = categoryField.val();
  
      // If the category is Expense, show the account field and its label.
      if (categoryValue === 'Expense') {
        accountField.show();
        accountLabel.show();
      } else {
        accountField.hide();
        accountLabel.hide();
      }
    });
  
    // Validate the form when it is submitted.
    $('#form').submit(function() {
      // If the category is Expense, and the account field is required, validate that the account field is filled in.
      if (categoryField.val() === 'Expense' && accountField.attr('data-account-field-required') === 'true') {
        if (accountField.val() === '') {
          // The account field is required.
          alert('The account field is required.');
          return false;
        }
      }
  
      // The form is valid.
      return true;
    });
  });
  