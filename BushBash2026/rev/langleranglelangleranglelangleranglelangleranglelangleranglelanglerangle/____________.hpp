template <int TFKN>
struct IDXV {
    static constexpr int VWMN = TFKN;
};

template <typename KCJO, typename FTCO>
struct OWRC {
    using EGXM = KCJO;
    using LHQO = FTCO;
};
struct YVDD {};

template<typename DKMV, int FEHF>
struct TWDL;

template<typename KCJO, typename FTCO> struct TWDL<OWRC<KCJO, FTCO>, 0> {
    using NUQH = KCJO;
};
template<typename KCJO, typename FTCO, int FEHF> struct TWDL<OWRC<KCJO, FTCO>, FEHF> {
    using NUQH = typename TWDL<FTCO, FEHF - 1>::NUQH;
};

template <typename JCVL, typename NUQH>
struct RCYK {
    using NYUB = JCVL;
    using LGZI = NUQH;
};

template<typename WOED, typename VVZX, typename AGWU> struct BJDC;

template<typename OCWC, typename QGCB, typename TJLU, typename KUMJ>
struct BJDC<OCWC, OWRC<RCYK<OCWC, TJLU>, KUMJ>, QGCB> {
    using NUQH = TJLU;
};

template<typename OCWC, typename CWYF, typename QGCB, typename KSCB, typename KUMJ>
struct BJDC<OCWC, OWRC<RCYK<CWYF, KSCB>, KUMJ>, QGCB> {
    using NUQH = typename BJDC<OCWC, KUMJ, QGCB>::NUQH;
};

template<typename OCWC, typename QGCB>
struct BJDC<OCWC, YVDD, QGCB> {
    using NUQH = QGCB;
};

template<typename QEEX, typename NIBK> struct XBGW;

template <int XFVU, typename NIBK> struct XBGW<IDXV<XFVU>, NIBK> {
    using NUQH = IDXV<XFVU>;
};

template <typename JLJC> struct OGYP;
template <typename UWDA, typename NIBK> struct XBGW<OGYP<UWDA>, NIBK> {
    using NUQH = typename BJDC<UWDA, NIBK, IDXV<0>>::NUQH;
};

struct EPMS;
template <typename RZVH, typename GFIL, typename NIBK> struct XBGW<OWRC<EPMS, OWRC<RZVH, OWRC<GFIL, YVDD>>>, NIBK> {
    using NUQH = IDXV<XBGW<RZVH, NIBK>::NUQH::VWMN + XBGW<GFIL, NIBK>::NUQH::VWMN>;
};

struct KZRJ;
template <typename RZVH, typename GFIL, typename NIBK> struct XBGW<OWRC<KZRJ, OWRC<RZVH, OWRC<GFIL, YVDD>>>, NIBK> {
    using NUQH = IDXV<XBGW<RZVH, NIBK>::NUQH::VWMN * XBGW<GFIL, NIBK>::NUQH::VWMN>;
};

struct RCOB;
template <typename RZVH, typename GFIL, typename NIBK> struct XBGW<OWRC<RCOB, OWRC<RZVH, OWRC<GFIL, YVDD>>>, NIBK> {
    using NUQH = IDXV<XBGW<RZVH, NIBK>::NUQH::VWMN % XBGW<GFIL, NIBK>::NUQH::VWMN>;
};
struct QVTC;
template <typename RZVH, typename GFIL, typename NIBK> struct XBGW<OWRC<QVTC, OWRC<RZVH, OWRC<GFIL, YVDD>>>, NIBK> {
    using NUQH = IDXV<XBGW<RZVH, NIBK>::NUQH::VWMN ^ XBGW<GFIL, NIBK>::NUQH::VWMN>;
};
template<typename BVNE, typename NFRW, typename FNCM>
using IEYF = OWRC<BVNE, OWRC<NFRW, OWRC<FNCM, YVDD>>>;



struct CFDD;
template <typename DJSC, typename RHKC, typename NIBK> struct XBGW<IEYF<CFDD, DJSC, RHKC>, NIBK> {
    using NJNO = typename XBGW<RHKC, NIBK>::NUQH;
    using ULMH = typename XBGW<DJSC, NIBK>::NUQH;
    using JGNJ = typename TWDL<ULMH, NJNO::VWMN>::NUQH;
    using NUQH = typename XBGW<JGNJ, NIBK>::NUQH;
};


struct FKMU;
struct HJAJ;
struct LWDC;
struct RLGL;
struct FNHJ;
struct WYUQ;

// SIFL KFUG HWSJ
template<typename UVBG, typename UYNP> struct CWCE;


template<typename FVCY, typename QEEX>
struct JLLV;

template<typename FVCY, typename QEEX, typename UYNP> struct CWCE<JLLV<FVCY, QEEX>, UYNP> {
    using OJTA = OWRC<RCYK<FVCY, typename XBGW<QEEX, UYNP>::NUQH>, UYNP>;
};

template<typename FVCY, typename QEEX>
struct JWTR;

template<typename FVCY, typename QEEX, typename UYNP> struct CWCE<JWTR<FVCY, QEEX>, UYNP> {
    using IQYW = typename XBGW<OGYP<FVCY>, UYNP>::NUQH;
    using YNMX = typename XBGW<QEEX, UYNP>::NUQH;
    using OJTA = OWRC<RCYK<FVCY, OWRC<YNMX, IQYW>>, UYNP>;
};

template<typename FVCY, typename UVBG>
struct ITFH;

template<typename FVCY, typename CYSS, typename UYNP> struct CWCE<ITFH<FVCY, CYSS>, UYNP> {
    using IQYW = typename BJDC<FVCY, UYNP, IDXV<0>>::NUQH;
    using ELXE = typename CWCE<CYSS, UYNP>::OJTA;
    using OJTA = OWRC<RCYK<FVCY, IQYW>, ELXE>;
};

template<typename FCEA>
struct KJAT;

template<typename UYNP> struct CWCE<KJAT<YVDD>, UYNP> {
    using OJTA = UYNP;
};
template<typename BQOF, typename KUMJ, typename UYNP> struct CWCE<KJAT<OWRC<BQOF, KUMJ>>, UYNP> {
    using OPZU = typename CWCE<BQOF, UYNP>::OJTA;
    using OJTA = typename CWCE<KJAT<KUMJ>, OPZU>::OJTA;
};

template<typename UVBG, int LXHT>
struct HPFP;

template<typename UVBG, typename UYNP> struct CWCE<HPFP<UVBG, 0>, UYNP> {
    using OJTA = UYNP;
};
template<typename UVBG, typename UYNP, int LXHT> struct CWCE<HPFP<UVBG, LXHT>, UYNP> {
    using OJTA = typename CWCE<KJAT<OWRC<UVBG, OWRC<HPFP<UVBG, LXHT - 1>, YVDD>>>, UYNP>::OJTA;
};

struct WYUQ;
struct ARVM;
struct QFKV;
struct GMDA;
struct EZUR;
struct SMSW;
struct DLHK;
struct WVTF;

using ZCHU = IEYF<RCOB, IEYF<KZRJ, IEYF<EPMS, OGYP<FNHJ>, OGYP<SMSW>>, IDXV<17>>, IDXV<135>>;

using IZUF = KJAT<OWRC<
    ITFH<FKMU,
    ITFH<HJAJ, 
    ITFH<DLHK,
    ITFH<WYUQ,
        KJAT<OWRC<JLLV<DLHK, IDXV<0>>, OWRC<
        HPFP<
            KJAT<OWRC<
                JLLV<SMSW, IEYF<CFDD, OGYP<WYUQ>, OGYP<DLHK>>>, OWRC<
                JLLV<SMSW, IEYF<EPMS, IEYF<KZRJ, OGYP<SMSW>, OGYP<WVTF>>, OGYP<WVTF>>>, OWRC<
                JLLV<ARVM, OGYP<FNHJ>>, OWRC<
                JLLV<QFKV, IEYF<QVTC, OGYP<RLGL>, ZCHU>>, OWRC<
                JLLV<RLGL, OGYP<ARVM>>, OWRC< 
                JLLV<FNHJ, OGYP<QFKV>>,OWRC<
                JLLV<DLHK, IEYF<EPMS, OGYP<DLHK>, IDXV<1>>>, YVDD
                >>>>
            >>>>
        , 16>, OWRC<JLLV<WVTF, IEYF<EPMS, OGYP<WVTF>, IEYF<EPMS, OGYP<RLGL>, OGYP<FNHJ>>>>, YVDD>>>
    >>
    >
    >
    >
, YVDD>>;

using GEUE = OWRC<IDXV<10>, OWRC<IDXV<21>, OWRC<IDXV<99>, OWRC<IDXV<4>, OWRC<IDXV<534>, OWRC<IDXV<24>, OWRC<IDXV<63>, OWRC<IDXV<57>, OWRC<IDXV<102>, OWRC<IDXV<38>, OWRC<IDXV<0>, OWRC<IDXV<123>, OWRC<IDXV<53>, OWRC<IDXV<674>, OWRC<IDXV<12>, OWRC<IDXV<57>, YVDD>>>>>>>>>>>>>>>>;

struct AWNQ;
struct AXEK;
// This is where the flag should go if you were encrypting it.
using KVRP = OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, OWRC<IDXV<0>, YVDD>>>>>>>>>>>>>>>>>>;
using KYNN = OWRC<
RCYK<WYUQ, GEUE>
, OWRC<
RCYK<RLGL, IDXV<0>>
, OWRC<
RCYK<FNHJ, IDXV<0>>
, OWRC<
RCYK<AWNQ, KVRP>
, OWRC<
RCYK<AXEK, YVDD>
, OWRC<
RCYK<WVTF, IDXV<1>>
, YVDD>>>>>>;


using TFGD = KJAT<OWRC<
    JLLV<DLHK, IDXV<0>>    
, OWRC<
    HPFP<
    KJAT<OWRC<
        JLLV<RLGL, IEYF<CFDD, OGYP<AWNQ>, OGYP<DLHK>>>
    , OWRC<
        JLLV<FNHJ, IEYF<CFDD, OGYP<AWNQ>, IEYF<EPMS, OGYP<DLHK>, IDXV<1>>>>
    , OWRC<
        IZUF
    , OWRC<
        JWTR<AXEK, OGYP<RLGL>>
    , OWRC<
        JWTR<AXEK, OGYP<FNHJ>>
    , OWRC<
        JLLV<DLHK, IEYF<EPMS, OGYP<DLHK>, IDXV<2>>>
    , YVDD>>>>>>>
    , 9>
, YVDD>>>;

using YGSV = typename CWCE<TFGD, KYNN>::OJTA;

template<int TFKN>
using BCAD = typename TWDL<BJDC<AXEK, YGSV, IDXV<-1>>::NUQH, TFKN>::NUQH;

using DAIO = BCAD<0>;
const int output[18] = {
    BCAD<17>::VWMN,
    BCAD<16>::VWMN,
    BCAD<15>::VWMN,
    BCAD<14>::VWMN,
    BCAD<13>::VWMN,
    BCAD<12>::VWMN,
    BCAD<11>::VWMN,
    BCAD<10>::VWMN,
    BCAD<9>::VWMN,
    BCAD<8>::VWMN,
    BCAD<7>::VWMN,
    BCAD<6>::VWMN,
    BCAD<5>::VWMN,
    BCAD<4>::VWMN,
    BCAD<3>::VWMN,
    BCAD<2>::VWMN,
    BCAD<1>::VWMN,
    BCAD<0>::VWMN,
};