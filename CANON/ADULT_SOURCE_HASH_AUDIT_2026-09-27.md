# Adult source/profile raw-file hash audit — 2026-09-27

Scope: all 22 registered adults, 44 current Drive files. This is a file-identity audit, not a new artwork approval or a full visual canon certification. No PNG or Word profile was changed. Drive remains the visual authority.

Findings: 14 source PNG hashes and 12 Word profile hashes differed from the previous GitHub registry; Elena Rivera and Marcus Jackson had no profile hash there. Eight adult pairs already matched. All 44 fresh raw downloads matched the independently downloaded files from the preceding height/color review. Each of the 22 current PNGs was found byte-for-byte inside its paired Word profile. The existing paired sources were visually reviewed in that preceding review. No historical cause or unrecorded approval is inferred from the mismatches.

Resolution: reconcile only registered file hashes to the current authoritative Drive bytes, preserve the same Drive IDs, synchronize existing Elena/Marcus GitHub profile copies, and update the Drive character and SHA256 manifests. Preserve the old recorded hashes below for traceability. Source art, Word profile content, heights, colors, badge/emblem/sticker locks, and company asset hashes are unchanged.

Matthias Becker and Luis Mendoza profiles contain unused media left from a template. Their displayed matching source images are present; the extra Darius media is not referenced by `word/document.xml`. No profile cleanup was performed.

| Character | File | Drive ID | Previous registry SHA256 | Verified raw SHA256 | Finding |
|---|---|---|---|---|---|
| Mrs-Harper | image | `1a8RlfOktPoAQ__pLTtLIyaA3qidnPOaD` | `ac95bce80c63cafa60bc088555a4cf66dfe86147ce51342185d773cee825f288` | `ac95bce80c63cafa60bc088555a4cf66dfe86147ce51342185d773cee825f288` | MATCH |
| Mrs-Harper | profile | `1WFn924opY9kuG2ZWYukYBI97Xm6vytu0` | `965c95f7659d185929cd58030805f0224f9229e6f3c81ee8544b1e98aac49d34` | `965c95f7659d185929cd58030805f0224f9229e6f3c81ee8544b1e98aac49d34` | MATCH |
| Elena-Rivera | image | `1LMyoOO57gA-NQxgtF5poW7UPvfVjgqjP` | `b3d4c2bd169f86b5403c1563ba2b0702d4dac4b9e2d582ee07d4e04c9eef541e` | `7607cf26c2d548a98f73a50560138f6dedd68689c0ff0cdb4fdbccc893f4aada` | MISMATCH |
| Elena-Rivera | profile | `1nplm3aa__GwX4zVAlZ85usrKFuijLQdX` | `MISSING` | `4174fae06271098642cdae38c05c67712adbdc2785a312cbd670ca6b297e6099` | MISSING |
| Marcus-Jackson | image | `1Y9-w_J1cnz_abDKpIL8Iz5W1GfvA_8xh` | `d2bddfdf69ad5d95d88c9f8a0c052b2af2ea3fce7db7066adba37d3a20a05a26` | `742f5a2609f9fcce1fcf2c2fec466d6a1e0deb2d98f7716aa7410253ab29c76d` | MISMATCH |
| Marcus-Jackson | profile | `1fz_v6E5jSGrZD6LVdlDaVflPCloME6T5` | `MISSING` | `0e3dd0970d1849417b3577bb803e733e1e18e13347122c748cc71dc993b472f7` | MISSING |
| Omar-Haddad | image | `1O3aQjII-MCTJkKGXBFGnFKlkrVAEooFU` | `419080f6ed702e8c8156e334b58159a54b71e03d06f32f65781ad0ee394f042a` | `419080f6ed702e8c8156e334b58159a54b71e03d06f32f65781ad0ee394f042a` | MATCH |
| Omar-Haddad | profile | `1_3fVjalO6s29OKVUvaiDIyY-jDXgAsGZ` | `c8735b76a9aaba6b2beada69c8980d23a4be3f2a6ce3f4b70da8a1888ed5e2c4` | `c8735b76a9aaba6b2beada69c8980d23a4be3f2a6ce3f4b70da8a1888ed5e2c4` | MATCH |
| Darius-Cole | image | `19DwA63zOWkf0wzcRLEsirKVKAwRl6IoR` | `fb043570754af2414af4e1f2b359ceacfb94ff614288121c6f8750dab39d17ec` | `fb043570754af2414af4e1f2b359ceacfb94ff614288121c6f8750dab39d17ec` | MATCH |
| Darius-Cole | profile | `1bGxDE5g2ADoVMR0otnrduAXXk4hIM4UO` | `46f5ac7cdf77b3922c51613c3b47a0894c702f1915f10cc07935680f9cf450f6` | `46f5ac7cdf77b3922c51613c3b47a0894c702f1915f10cc07935680f9cf450f6` | MATCH |
| Matthias-Becker | image | `1SSu1FS_GU-TmvcaKpeo79WTEBYbWdSiA` | `f3d6a4a76a6c1656d3420bba3d7bca92cc20ae5658e6c5eddb61438187b22678` | `f3d6a4a76a6c1656d3420bba3d7bca92cc20ae5658e6c5eddb61438187b22678` | MATCH |
| Matthias-Becker | profile | `1AezDbqDE-fRxdzpMECr4thS1qQ_tzEJ_` | `9957b6d13fe1424ade48099aa4c68fb5f7f581fe65e6ce3ddd63de3baba4a37b` | `9957b6d13fe1424ade48099aa4c68fb5f7f581fe65e6ce3ddd63de3baba4a37b` | MATCH |
| Luis-Mendoza | image | `1cB-Kurd99KMyKaKmar4rYTnw0U1JCFCk` | `db71ce1351582e1a31dfdbca9a41762d3ebfa4fff387e90d757a59ac2e0e41b3` | `db71ce1351582e1a31dfdbca9a41762d3ebfa4fff387e90d757a59ac2e0e41b3` | MATCH |
| Luis-Mendoza | profile | `1iLVzifnM16EHL4xG2uhTFIs00uY33ByS` | `2ad1341d7357f351901a9f5af7a5b4175d8b439b98d95478e731eefe5fa6c296` | `2ad1341d7357f351901a9f5af7a5b4175d8b439b98d95478e731eefe5fa6c296` | MATCH |
| Priya-Patel | image | `19ZMf5fqX8WGlhs7I7tJx_iFgrdlgpe8e` | `921d2f25818fe76c8b3e65f287126f47c6f886a1d5f7a8328413bc933659cbdb` | `b1a053ca9f77df429b3e72f4c49fe1b59fc843557c55f37afcebe8d87b89fdab` | MISMATCH |
| Priya-Patel | profile | `1ZyHR-GirFpMwk8DcRqlJVpy0RHXUBKd6` | `781589121cefc603394cc23a52fec983b3eae3a2887748a33c86fc7506051641` | `28bb5fb860b59357006d7c2a89e7f43455f61799a6f07cccbab6308988173166` | MISMATCH |
| Daniel-Brooks | image | `1TVWd4mtznkx3tFEKNKF_TClF5VBPILey` | `0d44df43f7438303100b1513df74ed9a6101f4df3799d15f8e8882d03cded22c` | `5fc186933893463902db56efb8d6b3e8d97697b7751d798e580a488da7450087` | MISMATCH |
| Daniel-Brooks | profile | `1yk_XlyuOxhaKMIms-e7mwbCrviNKZrKZ` | `ca7e02e41c98d5ebb4f0f2107fb423c977201b7a9a0f7cc2eec59280e66c8327` | `a096423467027096ceb99c671bea8c6299b77334509d49452b98f64dfaf35553` | MISMATCH |
| Tony-Marino | image | `1FjL5YJLklpXpHnqHGZmVc8Ps87IgvJro` | `096c6eb25d0e7491b113209899c2821b8baeda1b14fb941546384068e8e13ef6` | `546d050489f5c7eea1992c84b5d9a84e59accf372e85cb840b306fc2123c2054` | MISMATCH |
| Tony-Marino | profile | `1tJnFRmAnXSViwGbNxi9-RAyuBz9KD9Uq` | `7d94e2604a25c8df705c6c9a50da85a32b63ffcee686a8342c0753a7c14b00cc` | `6000214c393c2ef573b46f4dec4886ffc4d9c18069567868429b51d5427fe313` | MISMATCH |
| Claire-Morgan | image | `1ApL7UT7gBmjU87isBkMIgmH7yfl6osGI` | `a0de9814bee9ec01085ecbc2e4c7aef4733c0e8d7d360ecc4512b7b605718bca` | `bd46f6dc36bb208cee8fc0070af3bd0ffff241cccfe6ff2a612b251893969758` | MISMATCH |
| Claire-Morgan | profile | `1e1eXCok2BoUhiI0EJMPlJbSrAOl-fGNl` | `05d9f854f79fb788a25bcf17a2dcded8fab177c27b39754b7222dfd0a8663d58` | `42db0cd80c79f22ac5ad453dc65cb15adbeacf568fe165e24ca275d7b4ea167d` | MISMATCH |
| Andre-Lewis | image | `19t86oLfRhIKYzmYNbusdw5_4tCDw7WXt` | `837f6a6af7416b67d23056a463573186de988ce1d007581457e9407100d49bb4` | `d6e75728c961e654827581c3c8caea89c81447c526f1a61a2c39a5f8f886cdc8` | MISMATCH |
| Andre-Lewis | profile | `18CwXMwvHtzpdfFHvRrwP6kt627X8OVuY` | `8acda1faf28f817c179f1d86837b65a4d209313c7a8fdbf6614f91b27b087561` | `d1dfa10496e849da73fef28653a2579c76fd701094ef6eac7af619efd725ea2c` | MISMATCH |
| Danny-Novak | image | `1nwcHFsFOjHeOwn5Ia8ojuH0aPkeruhXC` | `43199348ae93eaa1acfcbabee15f97a8d23aa56bc3d3978e653a9665b2d5e1e3` | `5b0292f915a515ed9e925af690a3faa0e6630267c628c031db1513b0741f593d` | MISMATCH |
| Danny-Novak | profile | `1kA8So6rSfZzlBka3W4C7afJRy40FxAVe` | `f2b3f769e5d1e839888c0ce07103b78f5f75810c9e9228f59a15744d6b42dae7` | `24ac7b7d0ab6b83b81214dbb3a4a0cf1fb5c82b852ee3ebec977d5dbc06d2585` | MISMATCH |
| Erik-Halvorsen | image | `1RTlNNdcM4OABk5cyx5ojrWXZ6T9uo2yl` | `40fa7a196f26bdfbca046aedfe47d3be38441b922d66f454504f1ac1a2830ba1` | `2c4fb079d7e07fe3645726a17e3c3e84fe6f74fab6107ea42c232de1f6fa7753` | MISMATCH |
| Erik-Halvorsen | profile | `1x2hsPULWLsbQz5P-9AKD2bijnhJM2qNQ` | `4cb928f3780e0b0178428cb743939b01cf53dc8f009ee6f81108c0a8d3e2dee1` | `8f8d9853f86e3992cef74a9c69caaac1326d05614b7307be0ba051e7c159eba0` | MISMATCH |
| Sam-Carter | image | `1Qi3rZ38Z9ECfoDh9INZtJKrhlNiQL8MM` | `dd11bc1301b98788b245927530c6b58f346be9766168c7847107c81db2f39c40` | `3f702485e094e601fbff168ec2048894d9c27706145c2995573bf557f2253b84` | MISMATCH |
| Sam-Carter | profile | `1kK4mZofl4ThreXAmEOiTfobtroYz73g8` | `0d871c14cac23d3367c791bede9ddb9e874a8b4420f53b18485c14492c3c181e` | `dc4defd6cce8d90bd14d59c057b3ae42813d13dcc5b508241cd7495acb070aa0` | MISMATCH |
| Hannah-Kowalski | image | `1dpTbrZcPD1B0IUZQqEI91ShVnrXdRJ3X` | `495151ee75761db90a1141e72d4835c75c80d975ec41d6df5033bae376746b41` | `d10c6a014440259cc71416518d228770c98e67e63b5135e50d572c2923e8d199` | MISMATCH |
| Hannah-Kowalski | profile | `1tYW3YSp7wUOd15lhtnFei86bk5ZQjJi0` | `7a3baee6814a82d3f3b866aabb710f126a1c8bbac29994a705f7ff6356b54f54` | `4d80f49b4cfa6c046649f8cd562b2806baa8087dbde2280f994327d5b009760a` | MISMATCH |
| Rebecca-Foster | image | `1V1Di0i9D2jR20yvGI2hcEw0yY5dj0qb8` | `91ddaef15c3e12a1350f4854a5700eb626efa3026ce9b92e276e25da3173f158` | `f76c9a49c36a19de5df570828d0b7f2ac327958f8588d842caa93f1871206269` | MISMATCH |
| Rebecca-Foster | profile | `1D8decViO9EqAkdoV26jGNTqw1opps8zx` | `f3c1e1b3f919e755315562632aa4f8ba70e5242270138790041d0a3431180808` | `dfe68127812706127d8ebbd6a1f6511b3023d150ff82fbb4b63d9bc339102330` | MISMATCH |
| Natalie-Chen | image | `1YDeJ77qoOWC38ImzZ-L8ssI9VOtVzyWb` | `f1474d438e99ef7e71951d084179eacbebb628a6faa0e0648d3c4842e4b47b08` | `16498fa5d8c2b994b9d674cb555efe732847fd5f5e86fa536a3c8caaf494e0bc` | MISMATCH |
| Natalie-Chen | profile | `1kexCprbvMpHthz30eyCKVWwuPx6KKCML` | `237a3581f485b311185985b8ffe93d3240a13c63a433da288251e8e024a204c4` | `58f8e9478b1dba7ee03396a330b365c6630c6cd98e4fab574889bf319483b6a4` | MISMATCH |
| Rafael-Martinez | image | `1EZwyjIPxGsllz_wDM5SKZTtNXwbtMqyg` | `53064a9ba5dbbf62ae3d92558b923c789b73aeabd9e27d6f05f491e06e0910e7` | `53064a9ba5dbbf62ae3d92558b923c789b73aeabd9e27d6f05f491e06e0910e7` | MATCH |
| Rafael-Martinez | profile | `1Wc3dRKOlp1tQhDu85x1rH5eRHBeNR_er` | `eef33ee8abcf313496cc1b82e6aa98d22198f3199fe8882e165f177dad308a1e` | `eef33ee8abcf313496cc1b82e6aa98d22198f3199fe8882e165f177dad308a1e` | MATCH |
| Marisol-Vega | image | `1KE81oMwAByCvB82ISJLnGEmNxbYVwmQ5` | `2d663422cec71d394d684b85f484f0f9c5fa48fc6d2a7a780bd51b892767a871` | `2d663422cec71d394d684b85f484f0f9c5fa48fc6d2a7a780bd51b892767a871` | MATCH |
| Marisol-Vega | profile | `1fb6kliVp8mMyQCn33RYO0VtfudvWQkzl` | `f419851838804c352a83a2ac02655bca592da708305afd4ab5bc2157b41b0712` | `f419851838804c352a83a2ac02655bca592da708305afd4ab5bc2157b41b0712` | MATCH |
| Adrian-Park | image | `1lgne6yQTzA8jdd-xRWDUsLsljdF3xsxt` | `407ba7bd5e47a0aa0603f6f07752c8f3335bbd55eb7c3f5407df181f9212236e` | `407ba7bd5e47a0aa0603f6f07752c8f3335bbd55eb7c3f5407df181f9212236e` | MATCH |
| Adrian-Park | profile | `1b413iqNNYc1IVnDeFm6FI9U6g_oRpI7M` | `8a08f8561b6926ce6838f1502eac11bbdef255e3776f98092e27075b5f59de4f` | `8a08f8561b6926ce6838f1502eac11bbdef255e3776f98092e27075b5f59de4f` | MATCH |
| Mayor-Thomas-Whitaker | image | `1mXnar5Tl1iBPSSP_MaL1Xq7YVNTKabXB` | `ba40724f087fffde31ce196b101732054bdde38ab9deadb1af1a3b87d8459c7b` | `0be2b5d1355c42c8a077ac38302e45d39c91add993411a0c11a87b916fa091f8` | MISMATCH |
| Mayor-Thomas-Whitaker | profile | `1sePhT5kayhUtmfDyTFQ4DyYU_k0lWzCw` | `6ce42293c7de9e74bc2eb02059fd67c49be7f4833404e081f9b713e5a31bf715` | `563aae37e50fa113ea92a54a50d28a7d4df652b5cad579055eeb650d5926403b` | MISMATCH |

## Drive manifest coverage

The SHA256 manifest lacked entries for seven newer adult pairs (Omar, Darius, Matthias, Luis, Rafael, Marisol, and Adrian). Their 14 verified file entries were added using their existing filenames.

Drive had prior profile hashes for Elena and Marcus even though GitHub omitted them:

| Character | Prior Drive profile SHA256 | Verified raw profile SHA256 |
|---|---|---|
| Elena-Rivera | `053667917b7589a4ce41be34919ecbc772929461c5020c59e08c85d65994e3ec` | `4174fae06271098642cdae38c05c67712adbdc2785a312cbd670ca6b297e6099` |
| Marcus-Jackson | `125f28f61e797748a65b6c230f110c7f09a54e12f25e9ef77f8864621973b7b5` | `0e3dd0970d1849417b3577bb803e733e1e18e13347122c748cc71dc993b472f7` |
