let mul_poly_naive p q =
  let n = Array.length p in
  let k = Array.length q in
  let m = Array.make (n + k) 0. in
  for i = 0 to n - 1 do
      for j = 0 to k - 1 do
        m.(i + j) <- m.(i + j) +. p.(i) *. q.(j)
      done
  done;
  m
;;
(*La complexité de cette fonction est O(kn)*)

type complexe = {re : float; im : float};;

let zero = {re = 0.; im = 0.};;
let un = {re = 1.; im = 0.};;

let conj z = {re = z.re; im = -. z.im};;

let add z1 z2 = {re = z1.re +. z2.re; im = z1.im +. z2.im};;

let mul z1 z2 = {re = z1.re *. z2.re -. z1.im *. z2.im; im = z1.re *. z2.im +. z1.im *. z2.re};;

let rec horner p x = 
  match p with
  | [] -> zero
  | t :: q -> add t (mul x (horner q x))
;;
(*L'intérêt de cette méthode est d'effectuer moins de multiplication que pour la méthode naïve (O(n)).*)

let rec divise p =
  let rec aux p p_odd p_even =
    match p with
    | [] -> p_odd, p_even
    | [_] -> failwith "le nombre de coefficient est impair"
    | a :: b :: q -> aux q (a :: p_odd) (b :: p_even)
  in aux p [] []
;;

let rec puiss w n =
  match n with
  | 0 -> un
  | _ -> puiss (mul w w) (n-1)
;;

let fft p w =
  let v = puiss w 2 in
  let p_odd, p_even = divise p in
  let l = ref [] in
  let n = List.length p in
  for i = n / 2 - 1 downto 0 do
    let p_o = horner p_odd (puiss v i) in
    let p_e = horner p_even (puiss v i) in
    let res = add p_o (mul (puiss w i) p_e) in
    l := res :: !l
  done;
  !l
;;

let rec est_puiss2 n =
  if n = 1 then true
  else (if n mod 2 = 0 then est_puiss2 (n / 2)
  else false)


let puiss2 l =
  let rec aux n li =
    match li with (* n est le nombre d'éléments déjà vus *)
    | [] -> if est_puiss2 n then [] else zero::(aux (n+1) [])
    | e::q -> e::(aux (n+1) q)
  in aux 0 l
;;

(* puiss2 [un;un;un;un;un] *)

let completer l =
  let rec aux n li = match li with
    | [] -> if n = 0 then [] else zero::aux (n-1) []
    | e::q -> e::aux n q in
  aux (List.length l) l
;;

(* completer [un;un;un] *)

let rec mul_ft l p =
  match l, p with
  | [], [] -> []
  | [], _ | _, [] -> failwith "Listes n'ont pas la même taille"
  | [a], [b] -> [mul a b]
  | t :: q, r :: s -> (mul t r) :: (mul_ft q s)
;;


let coeff r =
  let n = List.length r in
  let rec aux l =
    match l with
    | [] -> []
    | t::q -> (mul {re = 2./. (float (n - 1)); im = 0.} t) :: aux q
  in aux r;;


let mul_poly p q =
  let p', q' = completer p, completer q in
  let n = List.length p' in
  let theta = 2.*.3.14159265 /. float n in
  let w = {re = cos(theta); im = sin(theta)} in (* on peut aussi utiliser exp *)
  let ftp, ftq = fft p' w, fft q' w in
  let r = mul_ft ftp ftq in
  let rhat = fft r (conj w) in
  coeff rhat;;