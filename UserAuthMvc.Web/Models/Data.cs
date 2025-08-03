using System.ComponentModel.DataAnnotations;

namespace UserAuthMvc.Web.Models;



public class RegisterViewModel
{
    public string UserName { get; set; } = null!;
    [Required(ErrorMessage = "E-Mail is required.")]
    [EmailAddress(ErrorMessage = "Please enter a valid e-mail address.")]
    public string Email { get; set; } = null!;
    [Required(ErrorMessage = "Password is required.")]
    [StringLength(128, MinimumLength = 6, ErrorMessage = "The password can be at least 6 and at most 128 characters.")]
    public string Password { get; set; } = null!;
    [Required(ErrorMessage = "Password is required.")]
    [StringLength(128, MinimumLength = 6, ErrorMessage = "The password can be at least 6 and at most 128 characters.")]
    public string ConfirmPassword { get; set; } = null!;
}

public class LoginViewModel
{
    [Required(ErrorMessage = "E-Mail is required.")]
    [EmailAddress(ErrorMessage = "Please enter a valid e-mail address.")]
    public string Email { get; set; }
    [Required(ErrorMessage = "Password is required.")]
    [StringLength(128, MinimumLength = 6, ErrorMessage = "The password can be at least 6 and at most 128 characters.")]
    public string Password { get; set; }
}

public class ResetPasswordRequestViewModel
{
    [Required(ErrorMessage = "E-Mail is required.")]
    [EmailAddress(ErrorMessage = "Please enter a valid e-mail address.")]
    public string Email { get; set; }
}

public class ResetPasswordViewModel
{
    [Required(ErrorMessage = "Password is required.")]
    [StringLength(128, MinimumLength = 6, ErrorMessage = "The password can be at least 6 and at most 128 characters.")]
    public string Token { get; set; } = null!;
    [Required(ErrorMessage = "Password is required.")]
    [StringLength(128, MinimumLength = 6, ErrorMessage = "The password can be at least 6 and at most 128 characters.")]
    public string NewPassword { get; set; } = null!;
    [Required(ErrorMessage = "Password is required.")]
    [StringLength(128, MinimumLength = 6, ErrorMessage = "The password can be at least 6 and at most 128 characters.")]
    public string ConfirmPassword { get; set; } = null!;
}

public class Product
{
    public string name { get; set; }
    public double price { get; set; }
    public string image { get; set; }
    public string link { get; set; }
}
