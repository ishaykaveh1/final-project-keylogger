<input type="text" id="primetest" value="" />
<input type="button" onClick="communicate()" value="Check" />

<script type="text/javascript">
function get_factor(n)
{
 let sr = Math.sqrt(n)
 // try to find a factor that is not 1.
 for (let i=2; i<=sr; i+=1) {
 if (n%i === 0) // is n divisible by i?
 return i
 }
 return 1 // n is a prime.
} // End of get_factor function.

function communicate()
{ // communicate with the user.
 let i = document.getElementById("primetest").value; // get checked number, using DOM.
 // is it a valid input?
 if (isNaN(i) || (i <= 0) || (Math.floor(i) !== i) ) {
 alert("The checked object should be a whole positive number");
 return
 }
 if (i == 1) {
 alert("1 is not a prime");
 return
 }
 let factor = get_factor(i)
 if (factor === 1)
 alert(i + " is a prime")
 else
 alert(i + " is not a prime, " + i + "=" + i/factor +"x"+ factor)
} // End of communication function
</script>