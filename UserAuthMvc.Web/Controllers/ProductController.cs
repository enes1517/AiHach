using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using UserAuthMvc.Web.Models;
using System.Collections.Generic;
using System.Text;

namespace UserAuthMvc.Web.Controllers
{
    public class ProductController : Controller
    {
        public async Task<IActionResult> Search(string q)
        {
            if (string.IsNullOrEmpty(q))
                return View(new List<Product>());

            using (var client = new HttpClient())
            {
                var requestBody = new StringContent($"{{\"user_input\": \"{q}\"}}", Encoding.UTF8, "application/json");
                var response = await client.PostAsync("http://localhost:5000/analyze", requestBody);
                var json = await response.Content.ReadAsStringAsync();
                var root = JsonConvert.DeserializeObject<RootObject>(json);
                return View(root.products ?? new List<Product>());
            }
        }
    }

    public class RootObject
    {
        public List<Product> products { get; set; }
    }

    public class Product
    {
        public string name { get; set; }
        public double price { get; set; }
        public string image { get; set; }
    }
}


// using System.Net.Http;
// using System.Threading.Tasks;
// using Microsoft.AspNetCore.Mvc;
// using Newtonsoft.Json;
// using UserAuthMvc.Web.Models;
// using System.Collections.Generic;
// using System.Text;

// namespace UserAuthMvc.Web.Controllers
// {
//     public class ProductController : Controller
//     {
//         public async Task<IActionResult> Search(string q)
//         {
//             if (string.IsNullOrEmpty(q))
//                 return View(new List<Product>());

//             using (var client = new HttpClient())
//             {
//                 var requestBody = new StringContent($"{{\"user_input\": \"{q}\"}}", Encoding.UTF8, "application/json");
//                 var response = await client.PostAsync("http://localhost:5000/analyze", requestBody);
//                 var json = await response.Content.ReadAsStringAsync();
//                 var root = JsonConvert.DeserializeObject<RootObject>(json);
//                 return View(root.products ?? new List<Product>());
//             }
//         }
//     }

//     // Güncellenmiş response modelleri
//     public class RootObject
//     {
//         public List<Product> products { get; set; }
//         public string memory_response { get; set; }
//         public string explanation { get; set; }
//         public string message { get; set; }
//         public string source { get; set; }
//         public bool success { get; set; }
//         public string error { get; set; }
//     }

//     public class Product
//     {
//         // Hem title hem name property'si (API farklı field döndürebilir)
//         public string title { get; set; }
//         public string name { get; set; }
//         public double price { get; set; }
//         public string image { get; set; }
//         public string link { get; set; }
//         public string why_recommended { get; set; }
        
//         // Görüntüleme için helper property
//         public string DisplayName => !string.IsNullOrEmpty(title) ? title : name;
//     }
// }