TEMPLATE = """#include <bits/stdc++.h>

#define ll long long
#define pii pair<int, int>
#define pll pair<long, long>
#define pdd pair<double, double>
#define fastio ios_base::sync_with_stdio(false);cin.tie(0);cout.tie(0)
#define exists(x,CT) CT.find(x)!=CT.end()
#define mod 1000000007
#define umap unordered_map
#define uset unordered_set

using namespace std;

vector<bool> prime;

ll modex(ll x,ll n)
{
	if(!n) return 1;
    if(n&1) return (x*modex((x*x)%mod,(n-1)/2))%mod;
    else return modex((x*x)%mod,n/2);
}
ll modinv(ll n) 
{ 
	return modex(n,mod-2); 
}
void sieve(ll n) {
	prime.resize(n+1, true);
	for(ll p=2;p*p<=n;p++) {
		if(prime[p]) {
			for(int i=p*p;i<=n;i+=p) prime[i] = false;
		}
	}
}


void solve() {
	// type code here

}

int main(void) {
	fastio;
	int t; cin>>t;
	while(t--)
		solve();
	return 0;
}

"""