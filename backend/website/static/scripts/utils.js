//export const loadjQuery = () => {
//    return new Promise((resolve, reject) => {
//        if (typeof window.jQuery !== 'undefined') {
//			console.log('jQuery already loaded in login.js');
//            resolve(); // jQuery already loaded
//        } else {
//            const script = document.createElement('script');
//            script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js';
//            script.onload = resolve;
//            script.onerror = reject;
//            document.head.appendChild(script);
//        }
//    });
//};